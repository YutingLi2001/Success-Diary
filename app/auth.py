import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlmodel import Session
from app.models import User, UserCreate
from app.database import get_async_session
import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fastmail = FastMail(conf)

async def get_user_db(session = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        verification_url = f"{os.getenv('FRONTEND_URL')}/auth/verify?token={token}"
        
        message = MessageSchema(
            subject="Success Diary - Verify your email",
            recipients=[user.email],
            body=f"""
            <html>
                <body>
                    <h2>Welcome to Success Diary!</h2>
                    <p>Hello {user.display_name or 'there'},</p>
                    <p>Thank you for signing up! Please verify your email address by clicking the link below:</p>
                    <p><a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 14px 25px; text-decoration: none; border-radius: 4px;">Verify Email</a></p>
                    <p>Or copy and paste this link: {verification_url}</p>
                    <p>Best regards,<br>The Success Diary Team</p>
                </body>
            </html>
            """,
            subtype="html"
        )
        
        await fastmail.send_message(message)
        print(f"Verification email sent to {user.email} with token: {token}")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)