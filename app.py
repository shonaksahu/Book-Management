from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.future import select
from transformers import pipeline

# Configuration
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/bookdb"
SECRET_KEY = "your_secret_key"

# Database setup
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

# Models
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    year_published = Column(Integer, nullable=False)
    summary = Column(Text)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    review_text = Column(Text)
    rating = Column(Integer, nullable=False)

# Schemas
class BookSchema(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: str

    class Config:
        orm_mode = True

class ReviewSchema(BaseModel):
    book_id: int
    user_id: int
    review_text: str
    rating: int

    class Config:
        orm_mode = True

# AI Summarizer
summarizer = pipeline("summarization", model="/home/shonak/Documents/jktech/llama-3-model")

def generate_summary(content: str) -> str:
    summary = summarizer(content, max_length=100, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

# CRUD Operations
async def add_book(db: AsyncSession, book_data: dict):
    new_book = Book(**book_data)
    db.add(new_book)
    await db.commit()
    return new_book

async def get_all_books(db: AsyncSession):
    result = await db.execute(select(Book))
    return result.scalars().all()

async def get_book_by_id(db: AsyncSession, book_id: int):
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar()

# API Setup
app = FastAPI(title="Book Management System")

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/books")
async def create_book(book: BookSchema, db: AsyncSession = Depends(get_db)):
    return await add_book(db, book.dict())

@app.get("/books")
async def list_books(db: AsyncSession = Depends(get_db)):
    return await get_all_books(db)

@app.get("/books/{book_id}")
async def retrieve_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books/{book_id}/reviews")
async def add_review(book_id: int, review: ReviewSchema, db: AsyncSession = Depends(get_db)):
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    new_review = Review(book_id=book_id, **review.dict())
    db.add(new_review)
    await db.commit()
    return new_review

@app.get("/books/{book_id}/summary")
async def book_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    summary = generate_summary(book.summary)
    return {"book_summary": summary}
