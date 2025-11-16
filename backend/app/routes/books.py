import asyncio
from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from app.models.book import (
    BookRecommendationRequest, 
    BookResponse, 
    RecommendationResponse,
    CategoriesResponse,
    TonesResponse
)
from app.services.recommendation import (
    retrieve_semantic_recommendations,
    get_available_categories,
    get_available_tones
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Thread pool for CPU-bound operations
executor = ThreadPoolExecutor(max_workers=4)

@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: BookRecommendationRequest):
    """
    Get book recommendations with TRUE async processing
    """
    try:
        # Run CPU-bound vector search in thread pool (NON-BLOCKING)
        recommendations_df = await asyncio.to_thread(
            retrieve_semantic_recommendations,
            query=request.query,
            category=request.category,
            tone=request.tone,
            initial_top_k=request.initial_top_k,
            final_top_k=request.final_top_k
        )
        
        # Convert DataFrame to list of BookResponse (also async)
        books = await asyncio.to_thread(_convert_df_to_books, recommendations_df)
        
        return RecommendationResponse(
            books=books, 
            total=len(books),
            query=request.query,
            category=request.category,
            tone=request.tone
        )
    
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def _convert_df_to_books(recommendations_df: pd.DataFrame) -> List[BookResponse]:
    """Helper function to convert DataFrame to BookResponse list"""
    books = []
    for _, row in recommendations_df.iterrows():
        books.append(BookResponse(
            isbn13=str(row["isbn13"]),
            title=str(row["title"]),
            authors=str(row["authors"]),
            category=str(row.get("simple_categories", "Unknown")),
            thumbnail=str(row["large_thumbnail"]),
            description=str(row["description"]),
            average_rating=float(row["average_rating"]) if pd.notna(row["average_rating"]) else 0.0,
            num_pages=float(row["num_pages"]) if pd.notna(row["num_pages"]) else None,
            published_year=float(row["published_year"]) if pd.notna(row["published_year"]) else None,
            ratings_count=float(row.get("ratings_count", 0)) if pd.notna(row.get("ratings_count")) else None,
            joy=float(row.get("joy", 0)) if pd.notna(row.get("joy")) else None,
            surprise=float(row.get("surprise", 0)) if pd.notna(row.get("surprise")) else None,
            anger=float(row.get("anger", 0)) if pd.notna(row.get("anger")) else None,
            fear=float(row.get("fear", 0)) if pd.notna(row.get("fear")) else None,
            sadness=float(row.get("sadness", 0)) if pd.notna(row.get("sadness")) else None
        ))
    return books

@router.get("/categories", response_model=CategoriesResponse)
async def get_categories():
    """Get list of available book categories (async)"""
    try:
        categories = await asyncio.to_thread(get_available_categories)
        return CategoriesResponse(categories=categories)
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tones", response_model=TonesResponse)
async def get_tones():
    """Get list of available emotional tones"""
    try:
        tones = await asyncio.to_thread(get_available_tones)
        return TonesResponse(tones=tones)
    except Exception as e:
        logger.error(f"Error getting tones: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Reado API is running"}