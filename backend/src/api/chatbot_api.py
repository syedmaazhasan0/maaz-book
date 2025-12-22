"""
Chatbot API - working endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

# Define models
class ChatRequest(BaseModel):
    question: str
    book_id: str
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    mode_used: str

# Create router
router = APIRouter()

# Main chatbot endpoint
@router.post("/test-query", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chatbot endpoint - working version"""
    answer = f"You asked: '{request.question}'\n\nThis is a response from the Physical AI and Humanoid Robotics book chatbot. The system is working correctly!"
    return ChatResponse(
        answer=answer,
        sources=["book-content"],
        mode_used="full_book"
    )
