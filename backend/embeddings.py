"""
Embedding generation using various providers
Supports OpenAI, Gemini, and local embeddings
"""
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

from config import settings


class EmbeddingManager:
    """Manages embedding generation across different providers"""
    
    def __init__(self):
        """Initialize embedding manager based on configuration"""
        self.embeddings = self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """Initialize embeddings based on provider setting"""
        provider = settings.EMBEDDING_PROVIDER.lower()
        
        if provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set in environment variables")
            return OpenAIEmbeddings(
                openai_api_key=settings.OPENAI_API_KEY,
                model=settings.EMBEDDING_MODEL
            )
        
        elif provider == "gemini":
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not set in environment variables")
            return GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=settings.GEMINI_API_KEY
            )
        
        elif provider == "local":
            # Use HuggingFace embeddings for local inference
            return HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
        
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents
        
        Args:
            texts: List of text strings to embed
        
        Returns:
            List of embedding vectors
        """
        return self.embeddings.embed_documents(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query
        
        Args:
            text: Query text to embed
        
        Returns:
            Embedding vector
        """
        return self.embeddings.embed_query(text)

