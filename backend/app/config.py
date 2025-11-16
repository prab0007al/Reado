from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Reado API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API settings
    API_V1_PREFIX: str = "/api"
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    # Vector store settings
    VECTOR_DB_PERSIST_DIRECTORY: str = "./chroma_db"
    EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"
    
    # Data paths
    BOOKS_DATA_PATH: str = "data/books_with_emotions.csv"
    TAGGED_DESCRIPTIONS_PATH: str = "data/tagged_description.txt"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()
