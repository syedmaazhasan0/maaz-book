from typing import List
from src.services.retrieval_service import RetrievalService
from src.services.generation_service import GenerationService
from src.models.content_models import ContentChunk
from src.models.query_models import QueryRequest, QueryResponse


class RAGService:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.generation_service = GenerationService()
    
    def query_full_book(self, request: QueryRequest) -> QueryResponse:
        """
        Handle a query against the full book content
        """
        # Retrieve relevant chunks based on the question
        relevant_chunks = self.retrieval_service.retrieve_relevant_chunks(
            request.question, 
            top_k=5
        )
        
        # Generate an answer based on the retrieved chunks
        answer = self.generation_service.generate_answer(
            request.question, 
            relevant_chunks
        )
        
        # Extract source IDs from the chunks
        sources = [chunk.id for chunk in relevant_chunks]
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            mode_used="full_book"
        )
    
    def query_selected_text(self, request: QueryRequest) -> QueryResponse:
        """
        Handle a query against only the selected text
        """
        if not request.selected_text:
            raise ValueError("Selected text is required for selected_text mode")
        
        # Create a chunk from the selected text
        selected_chunks = self.retrieval_service.retrieve_from_selected_text(
            request.selected_text
        )
        
        # Generate an answer based on the selected text
        answer = self.generation_service.generate_answer(
            request.question,
            selected_chunks
        )
        
        # For selected text mode, we return a special source identifier
        sources = ["selected_text"]
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            mode_used="selected_text"
        )
    
    def process_query(self, request: QueryRequest) -> QueryResponse:
        """
        Process a query request, choosing between full-book and selected-text modes
        """
        if request.selected_text:
            # Use selected text mode
            return self.query_selected_text(request)
        else:
            # Use full book mode
            return self.query_full_book(request)