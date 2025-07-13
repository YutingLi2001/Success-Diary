from datetime import date
from sqlmodel import SQLModel, Field

class Entry(SQLModel, table=True):
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
