from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import datetime
from backend.src.services.rag_service import rag_service
from backend.src.services.embedding_service import embedding_service
from backend.src.services.qdrant_service import qdrant_service

router = APIRouter()

# Request and response models
class QueryRequest(BaseModel):
    query: str
    sessionId: Optional[str] = None
    useSelectedTextOnly: bool = False
    selectedText: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    sources: List[str]
    sessionId: str
    timestamp: str

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatSession(BaseModel):
    sessionId: str
    messages: List[ChatMessage]

@router.post("/query", response_model=QueryResponse)
async def query_chatbot(request: QueryRequest):
    """
    Query the RAG chatbot to get answers based on book content or selected text
    """
    try:
        # Validate input
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if request.useSelectedTextOnly and not request.selectedText:
            raise HTTPException(status_code=400, detail="Selected text is required when useSelectedTextOnly is true")

        # Process the query using RAG service
        if request.useSelectedTextOnly and request.selectedText:
            # Use selected text only mode
            response_text = await rag_service.process_query_with_selected_text(
                request.query,
                request.selectedText
            )
            sources = ["Selected text"]
        else:
            # Use standard RAG flow
            result = await rag_service.process_full_rag_query(request.query)
            response_text = result["response"]
            sources = result.get("sources", ["Retrieved content"])

        session_id = request.sessionId or f"session-{datetime.datetime.now().timestamp()}"

        return QueryResponse(
            response=response_text,
            sources=sources,
            sessionId=session_id,
            timestamp=datetime.datetime.now().isoformat()
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error processing query")

@router.post("/chat-session")
async def create_chat_session(session: ChatSession):
    """
    Create or update a chat session
    """
    try:
        # This is a placeholder implementation
        return {"sessionId": session.sessionId, "status": "session_created"}
    except Exception as e:
        logging.error(f"Error creating chat session: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error creating session")

@router.get("/chat-session/{session_id}")
async def get_chat_session(session_id: str):
    """
    Retrieve a chat session
    """
    try:
        # This is a placeholder implementation
        return {"sessionId": session_id, "messages": []}
    except Exception as e:
        logging.error(f"Error retrieving chat session: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving session")