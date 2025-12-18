"""
Configuration file for YouTube Chatbot Backend
Handles environment variables and settings
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "")
    
    # LLM Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")  # openai, gemini, or ollama
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")
    
    # Embedding Configuration
    EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "openai")  # openai, gemini, or local
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    
    # Vector DB Configuration
    VECTOR_DB_TYPE: str = os.getenv("VECTOR_DB_TYPE", "faiss")  # faiss or chroma
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "./vector_db")
    
    # RAG Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "3"))
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "chrome-extension://*").split(",")
    
    # Cache Configuration
    CACHE_DIR: str = os.getenv("CACHE_DIR", "./cache")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

