import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

import pandas as pd
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.config import get_settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
books_df = None
db_books = None
embeddings_model = None

def initialize_vector_store():
    """Initialize the vector store by loading existing ChromaDB from disk"""
    global books_df, db_books, embeddings_model
    
    settings = get_settings()
    
    try:
        # Load books data
        logger.info("Loading books data...")
        books_df = pd.read_csv(settings.BOOKS_DATA_PATH)
        
        # Add large thumbnail URLs
        books_df["large_thumbnail"] = books_df["thumbnail"] + "&fife=w800"
        books_df["large_thumbnail"] = np.where(
            books_df["large_thumbnail"].isna(),
            "/static/cover-not-found.jpg",
            books_df["large_thumbnail"],
        )
        logger.info(f"✓ Loaded {len(books_df)} books")
        
        # Initialize embeddings model
        logger.info("Loading embeddings model...")
        embeddings_model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
            # encode_kwargs removed - causes conflict
)
        logger.info("✓ Embeddings model loaded")
        
        # Load existing ChromaDB from disk
        persist_dir = settings.VECTOR_DB_PERSIST_DIRECTORY
        
        if os.path.exists(persist_dir) and os.path.exists(os.path.join(persist_dir, "chroma.sqlite3")):
            logger.info("📂 Loading existing vector database from disk...")
            db_books = Chroma(
                persist_directory=persist_dir,
                embedding_function=embeddings_model
            )
            logger.info("✓ Vector database loaded successfully!")
        else:
            logger.error("❌ ChromaDB not found!")
            logger.error(f"❌ Expected location: {persist_dir}")
            logger.error("❌ Please create vector database using Google Colab first!")
            raise FileNotFoundError(
                f"Vector database not found at: {persist_dir}\n"
                "Create it using the Colab notebook, then download and extract chroma_db.zip here."
            )
        
        logger.info("=" * 60)
        logger.info("✓✓✓ INITIALIZATION COMPLETE ✓✓✓")
        logger.info(f"✓ Books loaded: {len(books_df)}")
        logger.info(f"✓ Vector DB: {persist_dir}")
        logger.info("=" * 60)
        return True
        
    except Exception as e:
        logger.error(f"❌ Error initializing vector store: {str(e)}")
        raise e

def get_books_dataframe():
    """Get the books DataFrame"""
    if books_df is None:
        raise RuntimeError("Books data not initialized. Call initialize_vector_store() first.")
    return books_df

def get_vector_db():
    """Get the vector database"""
    if db_books is None:
        raise RuntimeError("Vector DB not initialized. Call initialize_vector_store() first.")
    return db_books

def get_embeddings_model():
    """Get the embeddings model"""
    if embeddings_model is None:
        raise RuntimeError("Embeddings model not initialized. Call initialize_vector_store() first.")
    return embeddings_model