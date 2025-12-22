import pytest
from unittest.mock import Mock, patch
from src.services.rag_service import RAGService
from src.models.query_models import QueryRequest


def test_full_book_query():
    """
    Test that full-book query functionality works correctly
    """
    # Create a mock RAG service
    rag_service = RAGService()
    
    # Mock the retrieval service to return known chunks
    mock_chunk = Mock()
    mock_chunk.id = "test_chunk_id"
    mock_chunk.content = "This is test content for the book."
    
    with patch.object(rag_service.retrieval_service, 'retrieve_relevant_chunks', return_value=[mock_chunk]):
        # Mock the generation service to return a known answer
        with patch.object(rag_service.generation_service, 'generate_answer', return_value="This is the generated answer."):
            # Create a test request
            request = QueryRequest(
                question="What is this book about?",
                book_id="test_book_id"
            )
            
            # Process the query
            response = rag_service.query_full_book(request)
            
            # Verify the response
            assert response.answer == "This is the generated answer."
            assert response.sources == ["test_chunk_id"]
            assert response.mode_used == "full_book"


def test_selected_text_query():
    """
    Test that selected-text query functionality works correctly
    """
    # Create a mock RAG service
    rag_service = RAGService()
    
    # Mock the retrieval service to return a chunk from selected text
    mock_chunk = Mock()
    mock_chunk.id = "selected_text"
    mock_chunk.content = "This is the selected text."
    
    with patch.object(rag_service.retrieval_service, 'retrieve_from_selected_text', return_value=[mock_chunk]):
        # Mock the generation service to return a known answer
        with patch.object(rag_service.generation_service, 'generate_answer', return_value="This is the answer based on selected text."):
            # Create a test request with selected text
            request = QueryRequest(
                question="What does this selected text mean?",
                book_id="test_book_id",
                selected_text="This is the selected text."
            )
            
            # Process the query
            response = rag_service.query_selected_text(request)
            
            # Verify the response
            assert response.answer == "This is the answer based on selected text."
            assert response.sources == ["selected_text"]
            assert response.mode_used == "selected_text"


if __name__ == "__main__":
    test_full_book_query()
    test_selected_text_query()
    print("All tests passed!")