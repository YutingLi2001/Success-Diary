from datetime import date, datetime
from typing import Optional
import uuid
import re
from pydantic import EmailStr, validator
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel, Field
from fastapi_users import schemas
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

Base = declarative_base()

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    
    display_name: Optional[str] = Column(String(100), nullable=True)
    # Timezone handling fields (ADR-0005)
    user_timezone: Optional[str] = Column(String(50), nullable=True)  # Manual preference
    timezone_auto_detect: bool = Column(Boolean, default=True, nullable=False)  # Auto-detection enabled
    last_detected_timezone: Optional[str] = Column(String(50), nullable=True)  # Cache of last detected
    # Legacy timezone field (maintain compatibility)
    timezone: Optional[str] = Column(String(50), nullable=True, default="UTC")
    verification_code: Optional[str] = Column(String(6), nullable=True)
    verification_code_expires: Optional[datetime] = Column(DateTime, nullable=True)

class UserRead(schemas.BaseUser[uuid.UUID]):
    display_name: Optional[str]
    user_timezone: Optional[str]
    timezone_auto_detect: bool
    last_detected_timezone: Optional[str]
    timezone: Optional[str]  # Legacy field

class UserCreate(schemas.BaseUserCreate):
    display_name: Optional[str] = None
    user_timezone: Optional[str] = None
    timezone_auto_detect: bool = True
    last_detected_timezone: Optional[str] = None
    timezone: Optional[str] = "UTC"  # Legacy field

class UserUpdate(schemas.BaseUserUpdate):
    display_name: Optional[str] = None
    user_timezone: Optional[str] = None
    timezone_auto_detect: Optional[bool] = None
    last_detected_timezone: Optional[str] = None
    timezone: Optional[str] = None  # Legacy field

class Entry(SQLModel, table=True):
    __tablename__ = "entry"
    
    id: int | None = Field(default=None, primary_key=True)
    user_id: str
    entry_date: date
    success_1: str
    success_2: str | None = Field(default=None)
    success_3: str | None = Field(default=None)
    gratitude_1: str
    gratitude_2: str | None = Field(default=None)
    gratitude_3: str | None = Field(default=None)
    anxiety_1: str
    anxiety_2: str | None = Field(default=None)
    anxiety_3: str | None = Field(default=None)
    score: int
