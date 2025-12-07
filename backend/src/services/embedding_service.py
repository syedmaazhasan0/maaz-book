import openai
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmbeddingService:
    """
    Service for generating embeddings using OpenAI API
    """

    def __init__(self):
        # Set OpenAI API key from environment
        openai.api_key = os.getenv("OPENAI_API_KEY")

    async def create_embedding(self, text: str) -> List[float]:
        """
        Create an embedding for the given text
        """
        try:
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            embedding = response['data'][0]['embedding']
            return embedding
        except Exception as e:
            print(f"Error creating embedding: {e}")
            raise

    async def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for a batch of texts
        """
        embeddings = []
        for text in texts:
            embedding = await self.create_embedding(text)
            embeddings.append(embedding)
        return embeddings

# Global instance
embedding_service = EmbeddingService()