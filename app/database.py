from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"
engine = create_async_engine(DATABASE_URL, echo=False)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db() -> None:
    # Import all models to ensure they're registered
    from app.models import User, Entry, Base
    import os
    
    # Ensure the database directory exists and is writable
    db_path = "./db.sqlite3"
    if os.path.exists(db_path):
        print(f"Database file exists: {db_path}")
        print(f"Database file permissions: {oct(os.stat(db_path).st_mode)[-3:]}")
    else:
        print(f"Database file does not exist, will be created: {db_path}")
    
    try:
        async with engine.begin() as conn:
            # Create SQLAlchemy tables (for User)
            await conn.run_sync(Base.metadata.create_all)
            # Create SQLModel tables (for Entry)
            await conn.run_sync(SQLModel.metadata.create_all)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
        # Fallback to sync creation
        try:
            from sqlmodel import create_engine as sync_create_engine
            sync_engine = sync_create_engine("sqlite:///./db.sqlite3", echo=True)
            Base.metadata.create_all(sync_engine)
            SQLModel.metadata.create_all(sync_engine)
            print("Database created using sync fallback")
        except Exception as sync_error:
            print(f"Sync fallback also failed: {sync_error}")
            raise

async def get_async_session():
    async with async_session_maker() as session:
        yield session

# Keep sync session for SQLModel Entry operations
from sqlmodel import Session, create_engine as sync_create_engine
sync_engine = sync_create_engine("sqlite:///./db.sqlite3", echo=False)

def get_session():
    with Session(sync_engine) as session:
        yield session
