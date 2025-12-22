import time
import pytest
from unittest.mock import Mock, patch
from src.services.rag_service import RAGService
from src.models.query_models import QueryRequest


def test_response_time_performance():
    """
    Test that the system responds within 5 seconds for typical queries
    """
    rag_service = RAGService()
    
    # Mock the services to simulate normal operation without external dependencies
    with patch.object(rag_service.retrieval_service, 'retrieve_relevant_chunks') as mock_retrieval:
        with patch.object(rag_service.generation_service, 'generate_answer') as mock_generation:
            
            # Setup mock return values
            mock_chunk = Mock()
            mock_chunk.id = "perf_chunk_1"
            mock_chunk.content = "Artificial Intelligence is a wonderful field of computer science that creates intelligent machines."
            mock_chunk.book_id = "perf_book"
            mock_chunk.chunk_index = 0
            
            mock_retrieval.return_value = [mock_chunk]
            mock_generation.return_value = "Artificial Intelligence is a field of computer science that aims to create intelligent machines."
            
            # Create a test query
            request = QueryRequest(
                question="What is Artificial Intelligence?",
                book_id="perf_book"
            )
            
            # Measure the time it takes to process the query
            start_time = time.time()
            
            response = rag_service.query_full_book(request)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Verify the response time is under 5 seconds
            assert response_time < 5.0, f"Response time was {response_time:.2f}s, which exceeds 5 seconds"
            
            # Verify we got a valid response
            assert response.answer is not None
            assert len(response.answer) > 0
            
            print(f"Performance test passed: Response time was {response_time:.2f}s (under 5s target)")


def test_multiple_queries_performance():
    """
    Test performance with multiple queries to ensure consistent response times
    """
    rag_service = RAGService()
    
    # Mock the services
    with patch.object(rag_service.retrieval_service, 'retrieve_relevant_chunks') as mock_retrieval:
        with patch.object(rag_service.generation_service, 'generate_answer') as mock_generation:
            
            mock_chunk = Mock()
            mock_chunk.id = "multi_chunk_1"
            mock_chunk.content = "Machine learning is a subset of artificial intelligence that focuses on algorithms."
            mock_chunk.book_id = "multi_book"
            mock_chunk.chunk_index = 0
            
            mock_retrieval.return_value = [mock_chunk]
            mock_generation.return_value = "Machine learning is a subset of AI that uses algorithms to learn from data."
            
            questions = [
                "What is machine learning?",
                "How does machine learning work?",
                "What are applications of machine learning?",
                "Who invented machine learning?",
                "When was machine learning developed?"
            ]
            
            total_time = 0
            for question in questions:
                request = QueryRequest(
                    question=question,
                    book_id="multi_book"
                )
                
                start_time = time.time()
                response = rag_service.query_full_book(request)
                end_time = time.time()
                
                query_time = end_time - start_time
                total_time += query_time
                
                # Each query should be under 5 seconds
                assert query_time < 5.0, f"Query '{question}' took {query_time:.2f}s, exceeding 5s limit"
                
                # Verify response is valid
                assert response.answer is not None
                assert len(response.answer) > 0
            
            avg_time = total_time / len(questions)
            print(f"Multiple queries test passed: Average response time was {avg_time:.2f}s across {len(questions)} queries")


if __name__ == "__main__":
    test_response_time_performance()
    test_multiple_queries_performance()
    print("All performance tests passed!")