from fastapi import APIRouter
from typing import Dict

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint to verify the API is running and healthy
    """
    return {"status": "healthy", "message": "RAG Chatbot API is running"}

@router.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint for the API
    """
    return {"message": "Welcome to the RAG Chatbot API"}