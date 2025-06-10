from datetime import date
from sqlmodel import SQLModel, Field

class Entry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str
    entry_date: date
    success_1: str
    success_2: str
    success_3: str
    gratitude_1: str
    gratitude_2: str
    gratitude_3: str
    anxiety_1: str
    anxiety_2: str
    anxiety_3: str
    score: int
