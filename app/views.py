from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Book, Review
from app.serializers import BookCreate, BookResponse, ReviewCreate, ReviewResponse
from sqlalchemy.future import select
from typing import List

router = APIRouter()

# Add a new book
@router.post("/books", response_model=BookResponse)
async def add_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    new_book = Book(**book.dict())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

# Retrieve all books
@router.get("/books", response_model=List[BookResponse])
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    return result.scalars().all()

# Retrieve a specific book by its ID
@router.get("/books/{id}", response_model=BookResponse)
async def get_book(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter_by(id=id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Update a book's information by its ID
@router.put("/books/{id}", response_model=BookResponse)
async def update_book(id: int, book: BookCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter_by(id=id))
    existing_book = result.scalar_one_or_none()
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(existing_book, key, value)
    db.add(existing_book)
    await db.commit()
    await db.refresh(existing_book)
    return existing_book

# Delete a book by its ID
@router.delete("/books/{id}")
async def delete_book(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter_by(id=id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(book)
    await db.commit()
    return {"message": "Book deleted successfully"}

# Add a review for a book
@router.post("/books/{id}/reviews", response_model=ReviewResponse)
async def add_review(id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter_by(id=id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    new_review = Review(book_id=id, **review.dict())
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review

# Retrieve all reviews for a book
@router.get("/books/{id}/reviews", response_model=List[ReviewResponse])
async def get_reviews(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).filter_by(book_id=id))
    return result.scalars().all()
