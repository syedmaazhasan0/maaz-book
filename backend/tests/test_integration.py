import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from src.services.rag_service import RAGService
from src.models.query_models import QueryRequest


def test_full_rag_pipeline_integration():
    """
    Integration test for the full RAG pipeline
    Tests the flow: Query -> Retrieval -> Generation -> Response
    """
    rag_service = RAGService()
    
    # Mock all the services to avoid external dependencies in tests
    with patch.object(rag_service.retrieval_service, 'retrieve_relevant_chunks') as mock_retrieval:
        with patch.object(rag_service.generation_service, 'generate_answer') as mock_generation:
            
            # Setup mock return values
            mock_chunk = Mock()
            mock_chunk.id = "test_chunk_1"
            mock_chunk.content = "Artificial Intelligence is a wonderful field."
            mock_chunk.book_id = "test_book"
            mock_chunk.chunk_index = 0
            
            mock_retrieval.return_value = [mock_chunk]
            mock_generation.return_value = "Artificial Intelligence is a wonderful field that involves creating systems that can perform tasks typically requiring human intelligence."
            
            # Create a test query
            request = QueryRequest(
                question="What is Artificial Intelligence?",
                book_id="test_book"
            )
            
            # Execute the full pipeline
            response = rag_service.query_full_book(request)
            
            # Verify the results
            assert response.answer is not None
            assert len(response.answer) > 0
            assert response.sources == ["test_chunk_1"]
            assert response.mode_used == "full_book"
            
            # Verify that the services were called
            mock_retrieval.assert_called_once()
            mock_generation.assert_called_once()


def test_selected_text_pipeline_integration():
    """
    Integration test for the selected-text RAG pipeline
    """
    rag_service = RAGService()
    
    # Mock the services
    with patch.object(rag_service.retrieval_service, 'retrieve_from_selected_text') as mock_retrieval:
        with patch.object(rag_service.generation_service, 'generate_answer') as mock_generation:
            
            # Setup mock return values
            mock_chunk = Mock()
            mock_chunk.id = "selected_text"
            mock_chunk.content = "The theory of relativity was developed by Albert Einstein."
            mock_chunk.book_id = "selected"
            mock_chunk.chunk_index = 0
            
            mock_retrieval.return_value = [mock_chunk]
            mock_generation.return_value = "Albert Einstein developed the theory of relativity."
            
            # Create a test query with selected text
            request = QueryRequest(
                question="Who developed the theory of relativity?",
                book_id="test_book",
                selected_text="The theory of relativity was developed by Albert Einstein."
            )
            
            # Execute the selected-text pipeline
            response = rag_service.query_selected_text(request)
            
            # Verify the results
            assert response.answer == "Albert Einstein developed the theory of relativity."
            assert response.sources == ["selected_text"]
            assert response.mode_used == "selected_text"
            
            # Verify that the services were called
            mock_retrieval.assert_called_once()
            mock_generation.assert_called_once()


def test_rag_process_query_integration():
    """
    Integration test for the main process_query method
    """
    rag_service = RAGService()
    
    # Test full-book mode
    with patch.object(rag_service, 'query_full_book') as mock_full_book:
        with patch.object(rag_service, 'query_selected_text') as mock_selected_text:
            
            mock_response = Mock()
            mock_response.answer = "Test answer"
            mock_response.sources = ["test_source"]
            mock_response.mode_used = "full_book"
            
            mock_full_book.return_value = mock_response
            
            request = QueryRequest(
                question="Test question?",
                book_id="test_book"
            )
            
            response = rag_service.process_query(request)
            
            mock_full_book.assert_called_once_with(request)
            mock_selected_text.assert_not_called()
            assert response.mode_used == "full_book"
    
    # Test selected-text mode
    with patch.object(rag_service, 'query_full_book') as mock_full_book:
        with patch.object(rag_service, 'query_selected_text') as mock_selected_text:
            
            mock_response = Mock()
            mock_response.answer = "Test answer for selected text"
            mock_response.sources = ["selected_text"]
            mock_response.mode_used = "selected_text"
            
            mock_selected_text.return_value = mock_response
            
            request = QueryRequest(
                question="Test question?",
                book_id="test_book",
                selected_text="Selected text content"
            )
            
            response = rag_service.process_query(request)
            
            mock_selected_text.assert_called_once_with(request)
            mock_full_book.assert_not_called()
            assert response.mode_used == "selected_text"


if __name__ == "__main__":
    test_full_rag_pipeline_integration()
    test_selected_text_pipeline_integration()
    test_rag_process_query_integration()
    print("All integration tests passed!")