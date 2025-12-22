from typing import List
from src.services.qdrant_service import QdrantService
from src.services.embedding_service import EmbeddingService
from src.models.content_models import ContentChunk


class RetrievalService:
    def __init__(self):
        self.qdrant_service = QdrantService()
        self.embedding_service = EmbeddingService()
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[ContentChunk]:
        """
        Retrieve relevant content chunks based on the query
        """
        # Create embedding for the query
        query_embedding = self.embedding_service.create_single_embedding(query)
        
        # Search for similar vectors in Qdrant
        results = self.qdrant_service.search_similar(query_embedding, top_k)
        
        # Convert results back to ContentChunk objects
        relevant_chunks = []
        for result in results:
            payload = result["payload"]
            chunk = ContentChunk(
                id=payload.get("chunk_id", ""),
                content=payload.get("content", ""),
                book_id=payload.get("book_id", ""),
                chunk_index=payload.get("chunk_index", 0)
            )
            relevant_chunks.append(chunk)
        
        return relevant_chunks
    
    def retrieve_from_selected_text(self, selected_text: str) -> List[ContentChunk]:
        """
        Create a chunk from selected text and return it
        """
        # For selected text mode, we don't retrieve from storage
        # Instead, we create a temporary chunk from the selected text
        chunk = ContentChunk(
            id="selected_text",
            content=selected_text,
            book_id="selected",
            chunk_index=0
        )
        return [chunk]