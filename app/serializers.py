from pydantic import BaseModel
from typing import List, Optional

# Review Pydantic Models
class ReviewBase(BaseModel):
    user_id: int
    review_text: str
    rating: float

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int

    class Config:
        orm_mode = True

# Book Pydantic Models
class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    reviews: List[ReviewResponse] = []

    class Config:
        orm_mode = True
