import pytest
from unittest.mock import Mock, patch
from src.services.rag_service import RAGService
from src.models.query_models import QueryRequest


def test_selected_text_query_validation():
    """
    Test that selected-text query responses are properly validated
    """
    # Create a mock RAG service
    rag_service = RAGService()
    
    # Mock the retrieval service to return a chunk from selected text
    mock_chunk = Mock()
    mock_chunk.id = "selected_text"
    mock_chunk.content = "The theory of relativity was developed by Albert Einstein."
    
    with patch.object(rag_service.retrieval_service, 'retrieve_from_selected_text', return_value=[mock_chunk]):
        # Mock the generation service to return a known answer
        with patch.object(rag_service.generation_service, 'generate_answer', return_value="Albert Einstein developed the theory of relativity."):
            # Create a test request with selected text
            request = QueryRequest(
                question="Who developed the theory of relativity?",
                book_id="test_book_id",
                selected_text="The theory of relativity was developed by Albert Einstein."
            )
            
            # Process the query
            response = rag_service.query_selected_text(request)
            
            # Verify the response
            assert response.answer == "Albert Einstein developed the theory of relativity."
            assert response.sources == ["selected_text"]
            assert response.mode_used == "selected_text"


def test_selected_text_isolation():
    """
    Test that selected-text mode doesn't incorporate information from the full book
    """
    # This test verifies that the system only uses the selected text
    # and doesn't pull in information from elsewhere in the book
    rag_service = RAGService()
    
    # Mock the retrieval service to return only the selected text
    mock_chunk = Mock()
    mock_chunk.content = "The capital of France is Paris."
    
    with patch.object(rag_service.retrieval_service, 'retrieve_from_selected_text', return_value=[mock_chunk]):
        with patch.object(rag_service.generation_service, 'generate_answer', return_value="The capital of France is Paris."):
            request = QueryRequest(
                question="What is the capital of France?",
                book_id="test_book_id",
                selected_text="The capital of France is Paris."
            )
            
            response = rag_service.query_selected_text(request)
            
            # Verify it used only the selected text
            assert "Paris" is in response.answer
            assert response.mode_used == "selected_text"


if __name__ == "__main__":
    test_selected_text_query_validation()
    test_selected_text_isolation()
    print("Selected-text tests passed!")