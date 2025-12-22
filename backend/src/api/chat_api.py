"""
Simple chat API endpoints
"""
from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    book_id: str
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    mode_used: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, req: Request):
    """Simple chat endpoint"""
    answer = f"You asked: '{request.question}'. This is a response from the Physical AI chatbot system."
    return ChatResponse(
        answer=answer,
        sources=["book-content"],
        mode_used="full_book"
    )
