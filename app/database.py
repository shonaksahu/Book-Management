from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from databases import Database
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine
from app.models import Base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/bookmanagement"

# Database engine and session setup for async SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base for ORM models
Base = declarative_base()

# Database connection using databases package
database = Database(DATABASE_URL)

# Dependency to get the database session
async def get_db():
    async with SessionLocal() as session:
        yield session

# Create tables in the database
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
