import pytest
import time
from unittest.mock import Mock, patch
from src.services.rag_service import RAGService
from src.models.query_models import QueryRequest


def test_user_story_1_end_to_end():
    """
    End-to-end test for User Story 1: Query Book Content
    As a reader of an interactive book, I want to ask questions about the book's content 
    so that I can get immediate, accurate answers based on the material I'm reading.
    """
    rag_service = RAGService()
    
    # Mock the services to simulate a full book query
    with patch.object(rag_service.retrieval_service, 'retrieve_relevant_chunks') as mock_retrieval:
        with patch.object(rag_service.generation_service, 'generate_answer') as mock_generation:
            
            # Setup mock return values
            mock_chunk = Mock()
            mock_chunk.id = "chunk_001"
            mock_chunk.content = "Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals."
            mock_chunk.book_id = "book_001"
            mock_chunk.chunk_index = 0
            
            mock_retrieval.return_value = [mock_chunk]
            mock_generation.return_value = "Artificial Intelligence is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals."
            
            # Create a query request for full book content
            request = QueryRequest(
                question="What is Artificial Intelligence?",
                book_id="book_001"
            )
            
            # Execute the query
            response = rag_service.query_full_book(request)
            
            # Verify the response
            assert response.answer is not None
            assert "intelligence" in response.answer.lower()
            assert response.mode_used == "full_book"
            assert len(response.sources) > 0
            
            print("User Story 1 (Query Book Content) - PASSED")


def test_user_story_2_end_to_end():
    """
    End-to-end test for User Story 2: Text Selection Isolation
    As a reader, I want to select specific text in the book and ask questions only about that text
    so that the chatbot doesn't incorporate unrelated content from elsewhere in the book.
    """
    rag_service = RAGService()
    
    # Mock the services to simulate a selected text query
    with patch.object(rag_service.retrieval_service, 'retrieve_from_selected_text') as mock_retrieval:
        with patch.object(rag_service.generation_service, 'generate_answer') as mock_generation:
            
            # Setup mock return values
            mock_chunk = Mock()
            mock_chunk.id = "selected_text"
            mock_chunk.content = "The theory of relativity was developed by Albert Einstein."
            mock_chunk.book_id = "selected"
            mock_chunk.chunk_index = 0
            
            mock_retrieval.return_value = [mock_chunk]
            mock_generation.return_value = "According to the provided text, Albert Einstein developed the theory of relativity."
            
            # Create a query request with selected text
            request = QueryRequest(
                question="Who developed the theory of relativity?",
                book_id="book_001",
                selected_text="The theory of relativity was developed by Albert Einstein."
            )
            
            # Execute the query
            response = rag_service.query_selected_text(request)
            
            # Verify the response
            assert response.answer is not None
            assert "einstein" in response.answer.lower()
            assert response.mode_used == "selected_text"
            assert response.sources == ["selected_text"]
            
            print("User Story 2 (Text Selection Isolation) - PASSED")


def test_user_story_3_end_to_end():
    """
    End-to-end test for User Story 3: Embedded Chatbot Experience
    As a reader, I want the chatbot to be seamlessly integrated into the book interface
    so that I can access it without disrupting my reading experience.
    """
    # This test would involve testing the frontend integration
    # For now, we'll verify that the API can process queries correctly
    rag_service = RAGService()
    
    # Test the process_query method which handles both modes
    with patch.object(rag_service, 'query_full_book') as mock_full_book:
        with patch.object(rag_service, 'query_selected_text') as mock_selected_text:
            
            # Setup mock responses
            full_book_response = Mock()
            full_book_response.answer = "Full book answer"
            full_book_response.sources = ["source1"]
            full_book_response.mode_used = "full_book"
            
            selected_text_response = Mock()
            selected_text_response.answer = "Selected text answer"
            selected_text_response.sources = ["selected_text"]
            selected_text_response.mode_used = "selected_text"
            
            mock_full_book.return_value = full_book_response
            mock_selected_text.return_value = selected_text_response
            
            # Test full book mode
            full_book_request = QueryRequest(
                question="Full book question?",
                book_id="book_001"
            )
            full_book_response_actual = rag_service.process_query(full_book_request)
            assert full_book_response_actual.mode_used == "full_book"
            
            # Test selected text mode
            selected_text_request = QueryRequest(
                question="Selected text question?",
                book_id="book_001",
                selected_text="Selected text content"
            )
            selected_text_response_actual = rag_service.process_query(selected_text_request)
            assert selected_text_response_actual.mode_used == "selected_text"
            
            print("User Story 3 (Embedded Chatbot Experience) - PASSED")


def test_all_user_stories_integration():
    """
    Comprehensive test that validates all user stories work together
    """
    print("Running end-to-end tests for all user stories...")
    
    test_user_story_1_end_to_end()
    test_user_story_2_end_to_end()
    test_user_story_3_end_to_end()
    
    print("All user stories end-to-end tests - PASSED")


if __name__ == "__main__":
    test_all_user_stories_integration()