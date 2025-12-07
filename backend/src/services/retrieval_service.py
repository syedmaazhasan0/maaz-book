from typing import List, Dict, Any
from backend.src.services.qdrant_service import qdrant_service
from backend.src.services.embedding_service import embedding_service

class RetrievalService:
    """
    Service for handling document retrieval from vector store
    """

    async def retrieve_relevant_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant documents for a given query
        """
        try:
            # Create embedding for the query
            query_embedding = await embedding_service.create_embedding(query)

            # Query Qdrant for similar content
            search_results = await qdrant_service.query_vectors(query_embedding, top_k)

            return search_results
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            raise

    async def retrieve_with_selected_text(self, selected_text: str, query: str) -> str:
        """
        Return the selected text as context (for selected-text-only mode)
        """
        return selected_text

# Global instance
retrieval_service = RetrievalService()