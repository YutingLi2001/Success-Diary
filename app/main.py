from datetime import date
from typing import Optional
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
from pathlib import Path
from app.database import engine, init_db, get_session
from app.models import Entry, User, UserCreate, UserRead, UserUpdate
from app.auth import auth_backend, fastapi_users, current_active_user, current_verified_user
from fastapi.templating import Jinja2Templates

app = FastAPI()
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

@app.on_event("startup")
def on_startup() -> None:
    init_db()




async def get_current_user_safe(request: Request):
    try:
        return await current_active_user(request)
    except:
        return None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_session)):
    user = await get_current_user_safe(request)
    if user:
        entries = db.query(Entry).filter(Entry.user_id == str(user.id)).order_by(Entry.entry_date.desc()).all()
    else:
        entries = []
    return templates.TemplateResponse("index.html", {"request": request, "entries": entries, "user": user})


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@app.post("/add")
def add_entry(
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
    user: User = Depends(current_verified_user),
    db: Session = Depends(get_session),
):
    entry = Entry(
        user_id=str(user.id),
        entry_date=date.today(),
        success_1=success_1,
        success_2=success_2 if success_2.strip() else None,
        success_3=success_3 if success_3.strip() else None,
        gratitude_1=gratitude_1,
        gratitude_2=gratitude_2 if gratitude_2.strip() else None,
        gratitude_3=gratitude_3 if gratitude_3.strip() else None,
        anxiety_1=anxiety_1,
        anxiety_2=anxiety_2 if anxiety_2.strip() else None,
        anxiety_3=anxiety_3 if anxiety_3.strip() else None,
        score=score
    )
    db.add(entry)
    db.commit()
    return RedirectResponse("/", status_code=303)
