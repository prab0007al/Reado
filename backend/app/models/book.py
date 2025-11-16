from pydantic import BaseModel, Field
from typing import Optional, List

class BookRecommendationRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query for book recommendations")
    category: Optional[str] = Field(default="All", description="Book category filter")
    tone: Optional[str] = Field(default="All", description="Emotional tone filter")
    initial_top_k: int = Field(default=50, ge=1, le=100, description="Initial number of results to fetch")
    final_top_k: int = Field(default=16, ge=1, le=50, description="Final number of results to return")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "A story about forgiveness and redemption",
                "category": "Fiction",
                "tone": "Sad",
                "initial_top_k": 50,
                "final_top_k": 16
            }
        }

class BookResponse(BaseModel):
    isbn13: str
    title: str
    authors: str
    category: str
    thumbnail: str
    description: str
    average_rating: float
    num_pages: Optional[float] = None
    published_year: Optional[float] = None
    ratings_count: Optional[float] = None
    joy: Optional[float] = None
    surprise: Optional[float] = None
    anger: Optional[float] = None
    fear: Optional[float] = None
    sadness: Optional[float] = None

class RecommendationResponse(BaseModel):
    books: List[BookResponse]
    total: int
    query: str
    category: str
    tone: str

class CategoriesResponse(BaseModel):
    categories: List[str]

class TonesResponse(BaseModel):
    tones: List[str]
