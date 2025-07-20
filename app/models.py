from datetime import date, datetime
from typing import Optional
import uuid
import re
from pydantic import EmailStr, validator
from sqlalchemy import Column, String, DateTime, Boolean, event
from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel, Field
from fastapi_users import schemas
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

Base = declarative_base()

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    
    display_name: Optional[str] = Column(String(100), nullable=True)
    # Simplified timezone handling - auto-detection only
    last_detected_timezone: Optional[str] = Column(String(50), nullable=True)  # Browser detection cache
    # Legacy timezone field (maintain compatibility)
    timezone: Optional[str] = Column(String(50), nullable=True, default="UTC")
    verification_code: Optional[str] = Column(String(6), nullable=True)
    verification_code_expires: Optional[datetime] = Column(DateTime, nullable=True)

class UserRead(schemas.BaseUser[uuid.UUID]):
    display_name: Optional[str]
    last_detected_timezone: Optional[str]
    timezone: Optional[str]  # Legacy field

class UserCreate(schemas.BaseUserCreate):
    display_name: Optional[str] = None
    last_detected_timezone: Optional[str] = None
    timezone: Optional[str] = "UTC"  # Legacy field

class UserUpdate(schemas.BaseUserUpdate):
    display_name: Optional[str] = None
    last_detected_timezone: Optional[str] = None
    timezone: Optional[str] = None  # Legacy field

class Entry(SQLModel, table=True):
    __tablename__ = "entry"
    
    id: int | None = Field(default=None, primary_key=True)
    user_id: str
    entry_date: date
    title: str | None = Field(default=None)  # Auto-generated or custom title
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Exact timestamp when entry was created
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Exact timestamp when entry was last modified
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
    journal: str | None = Field(default=None)  # Free-form reflection field

# SQLAlchemy event listener to automatically update 'updated_at' timestamp
@event.listens_for(Entry, 'before_update')
def receive_before_update(mapper, connection, target):
    """Automatically set updated_at timestamp when entry is modified"""
    target.updated_at = datetime.utcnow()

class EntryUpdate(SQLModel):
    """Model for updating existing entries"""
    title: str | None = None
    success_1: str | None = None
    success_2: str | None = None
    success_3: str | None = None
    gratitude_1: str | None = None
    gratitude_2: str | None = None
    gratitude_3: str | None = None
    anxiety_1: str | None = None
    anxiety_2: str | None = None
    anxiety_3: str | None = None
    score: int | None = None
    journal: str | None = None
    
    @validator('score')
    def validate_score(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError('Score must be between 1 and 10')
        return v

class EntryRead(SQLModel):
    """Model for reading entries with timestamps"""
    id: int
    user_id: str
    entry_date: date
    title: str | None
    created_at: datetime
    updated_at: datetime
    success_1: str
    success_2: str | None
    success_3: str | None
    gratitude_1: str
    gratitude_2: str | None
    gratitude_3: str | None
    anxiety_1: str
    anxiety_2: str | None
    anxiety_3: str | None
    score: int
    journal: str | None
    
    @property
    def was_edited(self) -> bool:
        """Check if entry was edited after creation"""
        return self.updated_at > self.created_at
