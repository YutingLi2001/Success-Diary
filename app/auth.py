import uuid
from typing import Optional
from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.github import GitHubOAuth2
from sqlalchemy import update
from app.models import User, UserCreate
from app.database import get_async_session
import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")

# OAuth2 clients
google_oauth_client = GoogleOAuth2(
    os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
)

github_oauth_client = GitHubOAuth2(
    os.getenv("GITHUB_OAUTH_CLIENT_ID"), 
    os.getenv("GITHUB_OAUTH_CLIENT_SECRET")
)

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME") or "",
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD") or "",
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 1025)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    MAIL_STARTTLS=False,  # No TLS for local development
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,  # No auth needed for local SMTP
    VALIDATE_CERTS=False  # No cert validation for local
)

fastmail = FastMail(conf)

async def get_user_db(session = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


    # Using default FastAPI-Users reset_password implementation - no custom override needed

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        
        # Generate and send verification email immediately after registration
        import random
        from datetime import datetime, timedelta
        
        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Store the code in the user record with expiration
        from app.database import get_async_session
        from sqlalchemy import update
        async for session in get_async_session():
            # Update user with verification code using the user's ID to avoid session conflicts
            await session.execute(
                update(User)
                .where(User.id == user.id)
                .values(
                    verification_code=verification_code,
                    verification_code_expires=datetime.utcnow() + timedelta(minutes=10)
                )
            )
            await session.commit()
            break
        
        message = MessageSchema(
            subject="Success Diary - Verify your email",
            recipients=[user.email],
            body=f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #10b981; margin-bottom: 10px;">Welcome to Success Diary!</h1>
                        <p style="color: #6b7280; font-size: 16px;">Complete your registration</p>
                    </div>
                    
                    <div style="background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 24px; margin-bottom: 24px;">
                        <h2 style="color: #374151; margin-top: 0; margin-bottom: 16px;">Your verification code:</h2>
                        <div style="text-align: center; margin: 20px 0;">
                            <span style="display: inline-block; background-color: #10b981; color: white; font-size: 32px; font-weight: bold; padding: 12px 24px; border-radius: 8px; letter-spacing: 4px; font-family: 'Courier New', monospace;">
                                {verification_code}
                            </span>
                        </div>
                        <p style="color: #6b7280; margin-bottom: 0; text-align: center;">
                            Enter this code on the verification page to complete your registration.
                        </p>
                    </div>
                    
                    <div style="background-color: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 16px; margin-bottom: 24px;">
                        <p style="color: #92400e; margin: 0; font-size: 14px;">
                            <strong>⏰ Important:</strong> This code will expire in 10 minutes for security reasons.
                        </p>
                    </div>
                    
                    <div style="border-top: 1px solid #e5e7eb; padding-top: 20px; text-align: center;">
                        <p style="color: #9ca3af; font-size: 14px; margin: 0;">
                            If you didn't create this account, please ignore this email.
                        </p>
                        <p style="color: #9ca3af; font-size: 14px; margin: 8px 0 0 0;">
                            This is an automated message, please do not reply.
                        </p>
                    </div>
                </body>
            </html>
            """,
            subtype="html"
        )
        
        fm = FastMail(conf)
        try:
            await fm.send_message(message)
            print(f"Verification email sent to {user.email}: {verification_code}")
        except Exception as e:
            print(f"Failed to send verification email to {user.email}: {str(e)}")
    
    async def create(self, user_create, safe: bool = False, request: Optional[Request] = None):
        """Override create method to provide better error messages"""
        try:
            return await super().create(user_create, safe=safe, request=request)
        except UserAlreadyExists:
            raise HTTPException(
                status_code=400,
                detail="An account with this email already exists. Please try logging in instead."
            )

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        
        # Send password reset email
        reset_link = f"http://localhost:8000/auth/reset-password?token={token}"
        
        message = MessageSchema(
            subject="Success Diary - Password Reset",
            recipients=[user.email],
            body=f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #10b981;">Password Reset Request</h1>
                    </div>
                    
                    <div style="background-color: #f9fafb; padding: 30px; border-radius: 12px;">
                        <p style="color: #374151; margin-bottom: 20px;">Hi {user.display_name or user.email.split('@')[0]},</p>
                        
                        <p style="color: #374151; margin-bottom: 20px;">
                            We received a request to reset the password for your Success Diary account. 
                            If you didn't make this request, you can safely ignore this email.
                        </p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{reset_link}" 
                               style="display: inline-block; background-color: #3b82f6; color: white; 
                                      padding: 15px 30px; text-decoration: none; border-radius: 8px; 
                                      font-weight: bold; font-size: 16px;">
                                Reset My Password
                            </a>
                        </div>
                        
                        <p style="color: #6b7280; font-size: 14px; margin-bottom: 10px;">
                            Or copy and paste this link in your browser:
                        </p>
                        <p style="color: #3b82f6; font-size: 14px; word-break: break-all; 
                                  background-color: #f3f4f6; padding: 10px; border-radius: 4px;">
                            {reset_link}
                        </p>
                        
                        <p style="color: #ef4444; font-size: 14px; margin-top: 20px;">
                            ⏰ This link will expire in 1 hour for security reasons.
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px; color: #6b7280; font-size: 12px;">
                        <p>If you have any questions, please contact our support team.</p>
                        <p>© Success Diary - Your personal growth companion</p>
                    </div>
                </body>
            </html>
            """,
            subtype="html"
        )
        
        try:
            await fastmail.send_message(message)
            print(f"Password reset email sent to {user.email}")
        except Exception as e:
            print(f"Failed to send password reset email to {user.email}: {e}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # Generate a 6-digit verification code
        import random
        from datetime import datetime, timedelta
        
        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Store the code in the user record with expiration
        from app.database import get_async_session
        async for session in get_async_session():
            # Update user with verification code
            user.verification_code = verification_code
            user.verification_code_expires = datetime.utcnow() + timedelta(minutes=10)
            session.add(user)
            await session.commit()
            break
        
        message = MessageSchema(
            subject="Success Diary - Verify your email",
            recipients=[user.email],
            body=f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #10b981; margin-bottom: 10px;">Welcome to Success Diary!</h1>
                        <p style="color: #6b7280; font-size: 16px;">Complete your registration</p>
                    </div>
                    
                    <div style="background-color: #f9fafb; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 30px;">
                        <p style="color: #374151; font-size: 16px; margin-bottom: 20px;">
                            Hello {user.display_name or 'there'}! 👋
                        </p>
                        <p style="color: #6b7280; margin-bottom: 25px;">
                            To complete your registration, please enter this verification code:
                        </p>
                        
                        <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0; border: 2px solid #10b981;">
                            <h2 style="color: #10b981; font-size: 32px; font-weight: bold; margin: 0; letter-spacing: 8px;">
                                {verification_code}
                            </h2>
                        </div>
                        
                        <p style="color: #ef4444; font-size: 14px; margin-top: 15px;">
                            ⏰ This code expires in 10 minutes
                        </p>
                    </div>
                    
                    <div style="text-align: center; color: #6b7280; font-size: 14px;">
                        <p>If you didn't create an account, you can safely ignore this email.</p>
                        <p style="margin-top: 20px;">
                            Best regards,<br>
                            <strong>The Success Diary Team</strong>
                        </p>
                    </div>
                </body>
            </html>
            """,
            subtype="html"
        )
        
        await fastmail.send_message(message)
        print(f"Verification code sent to {user.email}: {verification_code}")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

cookie_transport = CookieTransport(cookie_name="access_token", cookie_max_age=3600)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)

# OAuth routers
google_oauth_router = fastapi_users.get_oauth_router(
    google_oauth_client,
    auth_backend,
    SECRET,
    associate_by_email=True,
    is_verified_by_default=True
)

github_oauth_router = fastapi_users.get_oauth_router(
    github_oauth_client, 
    auth_backend,
    SECRET,
    associate_by_email=True,
    is_verified_by_default=True
)