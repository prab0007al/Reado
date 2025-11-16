import pandas as pd
from typing import List
from app.services.vector_store import get_books_dataframe, get_vector_db
import logging

logger = logging.getLogger(__name__)

def retrieve_semantic_recommendations(
    query: str,
    category: str = "All",
    tone: str = "All",
    initial_top_k: int = 50,
    final_top_k: int = 16,
) -> pd.DataFrame:
    """
    Retrieve book recommendations based on semantic search
    
    Args:
        query: User's search query
        category: Book category filter
        tone: Emotional tone filter
        initial_top_k: Number of initial results from vector search
        final_top_k: Number of final results to return
    
    Returns:
        DataFrame containing recommended books
    """
    
    try:
        books = get_books_dataframe()
        db_books = get_vector_db()
        
        logger.info(f"Searching for: '{query}' with category='{category}', tone='{tone}'")
        
        # Perform semantic search
        recs = db_books.similarity_search(query, k=initial_top_k)
        
        # Extract ISBN13 from search results
        books_list = []
        for rec in recs:
            isbn_str = rec.page_content.strip('"').split()[0]
            try:
                books_list.append(int(isbn_str))
            except ValueError:
                logger.warning(f"Could not parse ISBN: {isbn_str}")
                continue
        
        logger.info(f"Found {len(books_list)} semantic matches")
        
        # Filter books by ISBNs
        book_recs = books[books["isbn13"].isin(books_list)].head(initial_top_k)
        
        # Filter by category if specified
        if category != "All":
            book_recs = book_recs[book_recs["simple_categories"] == category]
            logger.info(f"Filtered to {len(book_recs)} books in category '{category}'")
        
        # Limit to final_top_k
        book_recs = book_recs.head(final_top_k)
        
        # Sort by emotional tone if specified
        if tone == "Happy":
            book_recs = book_recs.sort_values(by="joy", ascending=False)
        elif tone == "Surprising":
            book_recs = book_recs.sort_values(by="surprise", ascending=False)
        elif tone == "Angry":
            book_recs = book_recs.sort_values(by="anger", ascending=False)
        elif tone == "Suspenseful":
            book_recs = book_recs.sort_values(by="fear", ascending=False)
        elif tone == "Sad":
            book_recs = book_recs.sort_values(by="sadness", ascending=False)
        
        logger.info(f"Returning {len(book_recs)} recommendations")
        return book_recs
        
    except Exception as e:
        logger.error(f"Error in recommendation service: {str(e)}")
        raise e

def get_available_categories() -> List[str]:
    """Get list of available book categories"""
    books = get_books_dataframe()
    categories = ["All"] + sorted(books["simple_categories"].dropna().unique().tolist())
    return categories

def get_available_tones() -> List[str]:
    """Get list of available emotional tones"""
    return ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]
