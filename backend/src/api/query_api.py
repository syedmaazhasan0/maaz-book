"""
Query API - RAG-enabled chatbot endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.services.simple_rag_service import SimpleRAGService
from src.models.query_models import QueryRequest as RAGQueryRequest

# Define models
class QueryRequest(BaseModel):
    question: str
    book_id: str
    selected_text: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    mode_used: str

# Create router
router = APIRouter()

# Initialize RAG service (using simple in-memory version for demo)
rag_service = SimpleRAGService()

# Main working endpoint with RAG
@router.post("/test-query", response_model=QueryResponse)
async def test_query(request: QueryRequest):
    """Main chatbot endpoint with RAG integration"""
    try:
        # Convert to RAG request format
        rag_request = RAGQueryRequest(
            question=request.question,
            book_id=request.book_id,
            selected_text=request.selected_text
        )

        # Process query using RAG service
        rag_response = rag_service.process_query(rag_request)

        # Return response
        return QueryResponse(
            answer=rag_response.answer,
            sources=rag_response.sources,
            mode_used=rag_response.mode_used
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# Main query endpoint with RAG
@router.post("/query", response_model=QueryResponse)
@router.post("/ask-question", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with RAG"""
    try:
        # Convert to RAG request format
        rag_request = RAGQueryRequest(
            question=request.question,
            book_id=request.book_id,
            selected_text=request.selected_text
        )

        # Process query using RAG service
        rag_response = rag_service.process_query(rag_request)

        return QueryResponse(
            answer=rag_response.answer,
            sources=rag_response.sources,
            mode_used=rag_response.mode_used
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# Alias endpoint for testing
@router.post("/ask", response_model=QueryResponse)
async def ask_endpoint(request: QueryRequest):
    """Ask endpoint with RAG"""
    try:
        # Convert to RAG request format
        rag_request = RAGQueryRequest(
            question=request.question,
            book_id=request.book_id,
            selected_text=request.selected_text
        )

        # Process query using RAG service
        rag_response = rag_service.process_query(rag_request)

        return QueryResponse(
            answer=rag_response.answer,
            sources=rag_response.sources,
            mode_used=rag_response.mode_used
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
