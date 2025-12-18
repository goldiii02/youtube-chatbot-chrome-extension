"""
FastAPI Backend Server for YouTube Chatbot Extension
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config import settings
from transcript_loader import TranscriptLoader
from rag_pipeline import RAGPipeline

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Chatbot API",
    description="RAG-based Q&A API for YouTube videos",
    version="1.0.0"
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
transcript_loader = TranscriptLoader(cache_dir=settings.CACHE_DIR)
rag_pipeline = RAGPipeline()

# Store current video processing state
video_cache = {}


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request model"""
    video_id: str
    user_query: str


class ChatResponse(BaseModel):
    """Chat response model"""
    answer: str
    success: bool
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(status="ok", message="YouTube Chatbot API is running")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="ok", message="API is healthy")


@app.post("/chat", response_model=ChatResponse)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def chat(request: Request, chat_request: ChatRequest):
    """
    Main chat endpoint for answering questions about YouTube videos
    
    Args:
        request: FastAPI request object (for rate limiting)
        chat_request: Chat request with video_id and user_query
    
    Returns:
        ChatResponse with answer or error
    """
    try:
        video_id = chat_request.video_id
        user_query = chat_request.user_query.strip()
        
        if not user_query:
            raise HTTPException(status_code=400, detail="User query cannot be empty")
        
        # Check if we need to process this video
        if video_id not in video_cache:
            # Fetch and process transcript
            try:
                transcript_data = transcript_loader.fetch_transcript(video_id)
                transcript_text = transcript_loader.get_full_text(video_id)
                
                # Process transcript through RAG pipeline
                rag_pipeline.process_transcript(video_id, transcript_text)
                
                # Cache the video ID
                video_cache[video_id] = True
                
            except ValueError as e:
                return ChatResponse(
                    answer="",
                    success=False,
                    error=str(e)
                )
        
        # Ensure RAG pipeline is set up for this video
        if rag_pipeline.current_video_id != video_id:
            transcript_text = transcript_loader.get_full_text(video_id)
            rag_pipeline.process_transcript(video_id, transcript_text)
            video_cache[video_id] = True
        
        # Get answer from RAG pipeline
        result = rag_pipeline.answer_question(user_query)
        
        return ChatResponse(
            answer=result["answer"],
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return ChatResponse(
            answer="",
            success=False,
            error=f"Internal server error: {str(e)}"
        )


@app.post("/reset/{video_id}")
async def reset_video(video_id: str):
    """
    Reset RAG pipeline for a specific video
    
    Args:
        video_id: YouTube video ID to reset
    """
    if video_id in video_cache:
        del video_cache[video_id]
    
    if rag_pipeline.current_video_id == video_id:
        rag_pipeline.reset()
    
    return {"status": "success", "message": f"Reset pipeline for video {video_id}"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )

