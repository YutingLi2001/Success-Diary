from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"
engine = create_async_engine(DATABASE_URL, echo=False)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def init_db() -> None:
    # Import all models to ensure they're registered
    from app.models import User, Entry, Base
    import asyncio
    
    async def create_tables():
        async with engine.begin() as conn:
            # Create SQLAlchemy tables (for User)
            await conn.run_sync(Base.metadata.create_all)
            # Create SQLModel tables (for Entry)
            await conn.run_sync(SQLModel.metadata.create_all)
    
    # Run the async function
    asyncio.create_task(create_tables())

async def get_async_session():
    async with async_session_maker() as session:
        yield session

# Keep sync session for SQLModel Entry operations
from sqlmodel import Session, create_engine as sync_create_engine
sync_engine = sync_create_engine("sqlite:///./db.sqlite3", echo=False)

def get_session():
    with Session(sync_engine) as session:
        yield session
