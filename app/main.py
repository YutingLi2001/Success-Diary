from datetime import date
from typing import Optional
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
from pathlib import Path
from app.database import engine, init_db, get_session
from app.models import Entry, EntryUpdate, EntryRead, User, UserCreate, UserRead, UserUpdate
from app.timezone_utils import get_user_local_date, format_user_timestamp, get_user_date_range
from app.auth import auth_backend, fastapi_users, current_active_user, current_verified_user, google_oauth_router, github_oauth_router
from fastapi.templating import Jinja2Templates

# Import error handling system
from app.errors import (
    http_exception_handler,
    authentication_error_handler,
    validation_error_handler,
    network_error_handler,
    general_exception_handler,
    AuthenticationError,
    ValidationError,
    NetworkError
)
from app.validation import get_client_validation_config, validate_daily_entry_server

app = FastAPI()

# Register error handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(AuthenticationError, authentication_error_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(NetworkError, network_error_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

# Include authentication routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Include OAuth routes
app.include_router(
    google_oauth_router,
    prefix="/auth/google",
    tags=["oauth"]
)
app.include_router(
    github_oauth_router,
    prefix="/auth/github", 
    tags=["oauth"]
)

@app.on_event("startup")
async def on_startup() -> None:
    await init_db()




async def get_current_user_safe(request: Request):
    """Safely get the current user without raising exceptions"""
    try:
        # Debug: Print all cookies
        cookies = request.cookies
        print(f"All request cookies: {cookies}")
        
        # The issue was calling current_active_user directly with request
        # We need to get the auth backend and call it properly
        from app.auth import auth_backend
        
        # Get the strategy and transport
        strategy = auth_backend.get_strategy()
        transport = auth_backend.transport
        
        # Read the token from the request - CookieTransport uses get_login_response method
        # Let's check what methods are available
        print(f"Transport methods: {[method for method in dir(transport) if not method.startswith('_')]}")
        
        # For CookieTransport, we need to get the token from cookies directly
        token = request.cookies.get("access_token")  # Use the cookie name we set
        if not token:
            print("No token found in cookies")
            return None
        
        print(f"Found token: {token[:50]}...")
        
        # Verify the token using strategy - let's decode manually for now
        import jwt
        import uuid
        from app.auth import SECRET
        
        try:
            # Decode the token to get user info - ignore audience for now
            payload = jwt.decode(token, SECRET, algorithms=["HS256"], options={"verify_aud": False})
            print(f"Token payload: {payload}")
            user_id_str = payload.get("sub")
            if not user_id_str:
                print("No user ID in token")
                return None
            
            print(f"Token user ID: {user_id_str}")
            
            # Convert string to UUID
            user_id = uuid.UUID(user_id_str)
            
            # Get user from database
            from app.auth import get_user_db
            from app.database import get_async_session
            
            async for session in get_async_session():
                async for user_db in get_user_db(session):
                    user = await user_db.get(user_id)
                    if user and user.is_active:
                        print(f"Found user: {user.email}, verified: {user.is_verified}")
                        return user
                    else:
                        print(f"User not found or inactive: {user_id}")
                        return None
                        
        except jwt.InvalidTokenError as e:
            print(f"JWT decode error: {e}")
            return None
                
    except Exception as e:
        print(f"Auth error: {type(e).__name__}: {e}")
        return None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_session)):
    user = await get_current_user_safe(request)
    if not user:
        print("No authenticated user, redirecting to login")
        return RedirectResponse("/login", status_code=303)
    
    print(f"User found: {user.email}, verified: {user.is_verified}")
    # For now, let's allow unverified users to access the dashboard
    entries = db.query(Entry).filter(Entry.user_id == str(user.id)).order_by(Entry.entry_date.desc()).limit(3).all()
    
    # Check if user can create entry today (one-entry-per-day constraint)
    db_user = db.query(User).filter(User.id == user.id).first()
    can_create_today = can_create_entry_today(db_user, db) if db_user else False
    existing_entry_today = None
    if not can_create_today and db_user:
        today_local = get_user_local_date(db_user)
        existing_entry_today = get_entry_for_date(db_user, today_local, db)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "entries": entries, 
        "user": user,
        "can_create_today": can_create_today,
        "existing_entry_today": existing_entry_today,
        "format_user_timestamp": format_user_timestamp
    })


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@app.get("/entries", response_class=HTMLResponse)
async def entries_page(request: Request, db: Session = Depends(get_session)):
    user = await get_current_user_safe(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    if not user.is_verified:
        return RedirectResponse("/verify?email=" + user.email, status_code=303)
    
    # Get all entries for the user
    entries = db.query(Entry).filter(Entry.user_id == str(user.id)).order_by(Entry.entry_date.desc()).all()
    
    # Calculate statistics
    total_entries = len(entries)
    avg_score = sum(e.score for e in entries) / total_entries if entries else 0
    
    # Group entries by year and month
    from collections import defaultdict
    from datetime import datetime
    import calendar
    
    entries_by_period = defaultdict(list)
    years = set()
    
    for entry in entries:
        year = entry.entry_date.year
        month = entry.entry_date.month
        years.add(year)
        
        # Note: search content will be generated in template for filtering
        
        period_key = f"{year}-{month:02d}"
        entries_by_period[period_key].append(entry)
    
    # Convert to list with metadata
    periods_list = []
    for period_key in sorted(entries_by_period.keys(), reverse=True):
        year, month = period_key.split('-')
        period_entries = entries_by_period[period_key]
        
        periods_list.append({
            'year': year,
            'month': month,
            'month_name': calendar.month_name[int(month)],
            'entries': sorted(period_entries, key=lambda x: x.entry_date, reverse=True),
            'avg_score': sum(e.score for e in period_entries) / len(period_entries)
        })
    
    # Calculate unique months and streak (simplified)
    unique_months = len(set((e.entry_date.year, e.entry_date.month) for e in entries))
    
    # Simple streak calculation (consecutive days with entries)
    streak_days = 0
    if entries:
        from datetime import date, timedelta
        current_date = date.today()
        entry_dates = set(e.entry_date for e in entries)
        
        while current_date in entry_dates:
            streak_days += 1
            current_date -= timedelta(days=1)
    
    return templates.TemplateResponse("entries.html", {
        "request": request, 
        "user": user,
        "entries_by_period": periods_list,
        "total_entries": total_entries,
        "avg_score": avg_score,
        "format_user_timestamp": format_user_timestamp,
        "unique_months": unique_months,
        "streak_days": streak_days,
        "years": sorted(years, reverse=True)
    })

@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    user = await get_current_user_safe(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    if not user.is_verified:
        return RedirectResponse("/verify?email=" + user.email, status_code=303)
    
    return templates.TemplateResponse("analytics.html", {"request": request, "user": user})

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    user = await get_current_user_safe(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    if not user.is_verified:
        return RedirectResponse("/verify?email=" + user.email, status_code=303)
    
    # Import here to avoid circular import
    # Simplified timezone handling - no manual override needed
    
    return templates.TemplateResponse("settings.html", {
        "request": request, 
        "user": user
    })


@app.get("/debug-auth")
async def debug_auth(request: Request):
    """Debug endpoint to check authentication status"""
    import jwt
    try:
        # Get token from cookies
        token = request.cookies.get("access_token")
        if not token:
            return {"error": "No token found", "cookies": dict(request.cookies)}
        
        # Decode the JWT token to see what's inside
        try:
            # First decode without verification to see the payload
            payload = jwt.decode(token, options={"verify_signature": False})
            return {
                "token_found": True,
                "token_payload": payload,
                "cookies": dict(request.cookies)
            }
        except Exception as jwt_error:
            return {
                "token_found": True,
                "jwt_decode_error": str(jwt_error),
                "cookies": dict(request.cookies)
            }
            
    except Exception as e:
        return {
            "authenticated": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "cookies": dict(request.cookies)
        }

@app.get("/test-dashboard", response_class=HTMLResponse)
async def test_dashboard(request: Request):
    """Simple test page that bypasses authentication"""
    return templates.TemplateResponse("test.html", {"request": request, "cookies": dict(request.cookies)})

@app.get("/verify", response_class=HTMLResponse)
async def verify_page(request: Request, email: str = ""):
    """Verification code input page"""
    return templates.TemplateResponse("auth/verify.html", {"request": request, "email": email})

@app.post("/auth/verify-code")
async def verify_code(request: Request):
    """Verify the 6-digit code"""
    from datetime import datetime
    import json
    
    body = await request.body()
    data = json.loads(body)
    email = data.get("email")
    code = data.get("code")
    
    if not email or not code:
        return {"detail": "Email and code are required"}, 400
    
    # Get user from database
    from app.database import get_async_session
    from app.auth import get_user_db
    
    async for session in get_async_session():
        async for user_db in get_user_db(session):
            # Find user by email
            from sqlalchemy import select
            from app.models import User
            
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            if not user:
                return {"detail": "User not found"}, 404
            
            # Check if code matches and hasn't expired
            if user.verification_code != code:
                return {"detail": "Invalid verification code"}, 400
            
            if user.verification_code_expires and user.verification_code_expires < datetime.utcnow():
                return {"detail": "Verification code has expired"}, 400
            
            # Verify the user
            user.is_verified = True
            user.verification_code = None
            user.verification_code_expires = None
            
            session.add(user)
            await session.commit()
            
            return {"message": "Email verified successfully"}
            
@app.post("/auth/resend-code")
async def resend_verification_code(request: Request):
    """Resend verification code"""
    import json
    import random
    from datetime import datetime, timedelta
    
    body = await request.body()
    data = json.loads(body)
    email = data.get("email")
    
    if not email:
        return {"detail": "Email is required"}, 400
    
    # Get user from database
    from app.database import get_async_session
    from app.auth import get_user_db
    
    async for session in get_async_session():
        async for user_db in get_user_db(session):
            from sqlalchemy import select
            from app.models import User
            
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            if not user:
                return {"detail": "User not found"}, 404
            
            # Generate new code
            verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            user.verification_code = verification_code
            user.verification_code_expires = datetime.utcnow() + timedelta(minutes=10)
            
            session.add(user)
            await session.commit()
            
            # Send email
            from app.auth import fastmail
            from fastapi_mail import MessageSchema
            
            message = MessageSchema(
                subject="Success Diary - New Verification Code",
                recipients=[user.email],
                body=f"""
                <html>
                    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #10b981;">New Verification Code</h1>
                        </div>
                        
                        <div style="background-color: #f9fafb; padding: 30px; border-radius: 12px; text-align: center;">
                            <p style="color: #374151; margin-bottom: 20px;">Here's your new verification code:</p>
                            
                            <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0; border: 2px solid #10b981;">
                                <h2 style="color: #10b981; font-size: 32px; font-weight: bold; margin: 0; letter-spacing: 8px;">
                                    {verification_code}
                                </h2>
                            </div>
                            
                            <p style="color: #ef4444; font-size: 14px;">⏰ This code expires in 10 minutes</p>
                        </div>
                    </body>
                </html>
                """,
                subtype="html"
            )
            
            await fastmail.send_message(message)
            print(f"New verification code sent to {user.email}: {verification_code}")
            
            return {"message": "New verification code sent"}


@app.post("/logout")
async def logout(request: Request):
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("access_token")
    return response


# One-entry-per-day constraint helper functions
def get_entry_for_date(user: User, target_date: date, db: Session) -> Entry | None:
    """
    Get existing entry for user on specific date.
    
    Args:
        user: User model instance
        target_date: Date to check in user's local timezone
        db: Database session
        
    Returns:
        Entry if exists, None otherwise
    """
    # Get UTC date range for the target date in user's timezone
    start_utc, end_utc = get_user_date_range(user, target_date)
    
    # Query for entries within this date range
    existing_entry = db.query(Entry).filter(
        Entry.user_id == str(user.id),
        Entry.created_at >= start_utc,
        Entry.created_at <= end_utc
    ).first()
    
    return existing_entry


def can_create_entry_today(user: User, db: Session) -> bool:
    """
    Check if user can create an entry for today.
    Implements simple one-entry-per-day constraint using auto-detected timezone.
    
    Args:
        user: User model instance
        db: Database session
        
    Returns:
        bool: True if user can create entry, False if already exists
    """
    today_local = get_user_local_date(user)  # Auto-detected timezone
    existing_entry = get_entry_for_date(user, today_local, db)
    return existing_entry is None


@app.post("/add")
async def add_entry(
    request: Request,
    title: str = Form(""),
    success_1: str = Form(...),
    success_2: str = Form(""),
    success_3: str = Form(""),
    gratitude_1: str = Form(...),
    gratitude_2: str = Form(""),
    gratitude_3: str = Form(""),
    anxiety_1: str = Form(...),
    anxiety_2: str = Form(""),
    anxiety_3: str = Form(""),
    score: int = Form(...),
    journal: str = Form(""),
    db: Session = Depends(get_session),
):
    # Get the current user using our safe method
    user = await get_current_user_safe(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    # Check if user is verified
    if not user.is_verified:
        return RedirectResponse("/verify?email=" + user.email, status_code=303)
    
    print(f"Adding entry for user: {user.email}, verified: {user.is_verified}")
    
    # Refresh user from sync database to get latest timezone settings
    # This ensures we have the most up-to-date timezone data for date calculation
    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        return RedirectResponse("/login", status_code=303)
    
    print(f"Refreshed user timezone data: detected={db_user.last_detected_timezone}, legacy={db_user.timezone}")
    
    # Check one-entry-per-day constraint
    if not can_create_entry_today(db_user, db):
        today_local = get_user_local_date(db_user)
        existing_entry = get_entry_for_date(db_user, today_local, db)
        
        # Return error with link to existing entry
        if request.headers.get("HX-Request"):
            return HTMLResponse(
                f'<div class="error-message">You already created an entry for {today_local.strftime("%B %d, %Y")}. '
                f'<a href="/entries/{existing_entry.id}" class="text-blue-600 hover:text-blue-800">View/Edit Entry</a></div>'
            )
        else:
            # For regular form submission, redirect to existing entry
            return RedirectResponse(f"/entries/{existing_entry.id}", status_code=303)
    
    entry = Entry(
        user_id=str(user.id),
        entry_date=get_user_local_date(db_user),  # Use refreshed user object
        title=title if title.strip() else None,
        success_1=success_1,
        success_2=success_2 if success_2.strip() else None,
        success_3=success_3 if success_3.strip() else None,
        gratitude_1=gratitude_1,
        gratitude_2=gratitude_2 if gratitude_2.strip() else None,
        gratitude_3=gratitude_3 if gratitude_3.strip() else None,
        anxiety_1=anxiety_1,
        anxiety_2=anxiety_2 if anxiety_2.strip() else None,
        anxiety_3=anxiety_3 if anxiety_3.strip() else None,
        score=score,
        journal=journal if journal.strip() else None
    )
    db.add(entry)
    db.commit()
    
    # Show success message for HTMX requests
    if request.headers.get("HX-Request"):
        return HTMLResponse('<div class="success-message">Entry saved successfully!</div>')
    
    return RedirectResponse("/", status_code=303)

@app.put("/entries/{entry_id}")
async def update_entry(
    entry_id: int,
    request: Request,
    title: str = Form(""),
    success_1: str = Form(""),
    success_2: str = Form(""),
    success_3: str = Form(""),
    gratitude_1: str = Form(""),
    gratitude_2: str = Form(""),
    gratitude_3: str = Form(""),
    anxiety_1: str = Form(""),
    anxiety_2: str = Form(""),
    anxiety_3: str = Form(""),
    score: int = Form(...),
    journal: str = Form(""),
    db: Session = Depends(get_session),
):
    """Update an existing entry"""
    # Get the current user
    user = await get_current_user_safe(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="User not verified")
    
    # Get the entry and verify ownership
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == str(user.id)).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # Update all fields since form always sends values
    update_data = {}
    update_data["title"] = title.strip() if title.strip() else None
    update_data["success_1"] = success_1.strip()
    update_data["success_2"] = success_2.strip() if success_2.strip() else None
    update_data["success_3"] = success_3.strip() if success_3.strip() else None
    update_data["gratitude_1"] = gratitude_1.strip()
    update_data["gratitude_2"] = gratitude_2.strip() if gratitude_2.strip() else None
    update_data["gratitude_3"] = gratitude_3.strip() if gratitude_3.strip() else None
    update_data["anxiety_1"] = anxiety_1.strip()
    update_data["anxiety_2"] = anxiety_2.strip() if anxiety_2.strip() else None
    update_data["anxiety_3"] = anxiety_3.strip() if anxiety_3.strip() else None
    update_data["journal"] = journal.strip() if journal.strip() else None
    
    # Validate score
    if score < 1 or score > 10:
        raise HTTPException(status_code=400, detail="Score must be between 1 and 10")
    update_data["score"] = score
    
    # Apply updates
    for field, value in update_data.items():
        setattr(entry, field, value)
    
    # The updated_at field will be automatically set by the SQLAlchemy event listener
    db.commit()
    db.refresh(entry)
    
    print(f"Entry {entry_id} updated successfully")
    return RedirectResponse("/entries", status_code=303)

@app.get("/entries/{entry_id}/view", response_class=HTMLResponse)
async def view_entry(
    entry_id: int,
    request: Request,
    db: Session = Depends(get_session)
):
    """View a specific entry in detail (read-only)"""
    # Get the current user
    user = await get_current_user_safe(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    if not user.is_verified:
        return RedirectResponse("/verify?email=" + user.email, status_code=303)
    
    # Get the entry and verify ownership
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == str(user.id)).first()
    if not entry:
        return RedirectResponse("/entries", status_code=303)
    
    return templates.TemplateResponse("entry_detail.html", {
        "request": request,
        "entry": entry,
        "user": user,
        "format_user_timestamp": format_user_timestamp
    })

@app.get("/entries/{entry_id}", response_class=HTMLResponse)
async def get_entry(
    entry_id: int,
    request: Request,
    db: Session = Depends(get_session)
):
    """Get a specific entry for editing"""
    # Get the current user
    user = await get_current_user_safe(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    if not user.is_verified:
        return RedirectResponse("/verify?email=" + user.email, status_code=303)
    
    # Get the entry and verify ownership
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == str(user.id)).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    return templates.TemplateResponse("edit_entry.html", {
        "request": request,
        "user": user,
        "entry": entry,
        "format_user_timestamp": format_user_timestamp
    })


# Test endpoints for error handling (development only)
@app.get("/test/errors")
async def test_errors_page(request: Request):
    """Development page to test different error types."""
    return templates.TemplateResponse("test/errors.html", {"request": request})


@app.post("/test/validation-error")
async def test_validation_error(request: Request):
    """Test validation error handling."""
    raise ValidationError("This is a test validation error. Please check your input.")


@app.post("/test/auth-error")
async def test_auth_error(request: Request):
    """Test authentication error handling."""
    raise AuthenticationError("Your session has expired. Please sign in again.")


@app.post("/test/network-error")
async def test_network_error(request: Request):
    """Test network error handling."""
    raise NetworkError("Connection to external service failed.")


@app.post("/test/server-error")
async def test_server_error(request: Request):
    """Test server error handling."""
    raise Exception("This is a test server error.")


@app.post("/test/http-error")
async def test_http_error(request: Request):
    """Test HTTP error handling."""
    raise HTTPException(status_code=404, detail="Test resource not found")


# Timezone management endpoints
@app.post("/api/user/update-detected-timezone")
async def update_detected_timezone(
    request: Request,
    user: User = Depends(current_active_user)
):
    """Simple auto-detection timezone update."""
    try:
        data = await request.json()
        detected = data.get('detected_timezone')
        
        if detected:
            # Update detected timezone in sync database
            db = next(get_session())
            db_user = db.query(User).filter(User.id == user.id).first()
            
            if db_user:
                db_user.last_detected_timezone = detected
                db.commit()
                print(f"Updated detected timezone for {user.email}: {detected}")
        
        return {"success": True, "detected_timezone": detected}
        
    except Exception as e:
        print(f"Error updating detected timezone: {e}")
        raise HTTPException(status_code=400, detail="Failed to update timezone")


# Validation configuration endpoint
@app.get("/api/validation-config/{form_type}")
async def get_validation_config(form_type: str):
    """Get validation configuration for client-side JavaScript."""
    config = get_client_validation_config(form_type)
    return {"config": config}
