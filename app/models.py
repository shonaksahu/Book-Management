from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    year_published = Column(Integer, nullable=True)
    summary = Column(Text, nullable=True)

    reviews = relationship("Review", back_populates="book")


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    review_text = Column(Text)
    rating = Column(Float)

    book = relationship("Book", back_populates="reviews")
