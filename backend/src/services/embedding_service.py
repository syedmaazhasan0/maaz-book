from typing import List
from src.services.cohere_service import CohereClient
from src.models.content_models import ContentChunk


class EmbeddingService:
    def __init__(self):
        self.cohere_client = CohereClient()
    
    def create_embeddings(self, chunks: List[ContentChunk]) -> List[List[float]]:
        """
        Create embeddings for the provided content chunks
        """
        # Extract text content from chunks
        texts = [chunk.content for chunk in chunks]
        
        # Generate embeddings using Cohere
        embeddings = self.cohere_client.embed_texts(texts)
        
        return embeddings
    
    def create_single_embedding(self, text: str) -> List[float]:
        """
        Create embedding for a single text (used for query embedding)
        """
        embeddings = self.cohere_client.embed_texts([text])
        return embeddings[0]