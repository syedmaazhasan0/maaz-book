from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
from backend.src.models.chapter import ContentChunk

# Load environment variables
load_dotenv()

class QdrantService:
    """
    Service for interacting with Qdrant vector database
    """

    def __init__(self):
        # Initialize Qdrant client with environment variables
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            prefer_grpc=True  # Use gRPC for better performance
        )
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

    def create_collection(self, vector_size: int = 1536):
        """
        Create a collection in Qdrant for storing embeddings
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]

            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE
                    )
                )
                print(f"Collection '{self.collection_name}' created successfully")
            else:
                print(f"Collection '{self.collection_name}' already exists")
        except Exception as e:
            print(f"Error creating collection: {e}")
            raise

    async def insert_vectors(self, chunks: List[ContentChunk]):
        """
        Insert content chunks with their embeddings into Qdrant
        """
        try:
            points = []
            for chunk in chunks:
                point = PointStruct(
                    id=chunk.id,
                    vector=chunk.embedding,
                    payload={
                        "content": chunk.content,
                        "chapter_id": chunk.chapterId,
                        "chunk_index": chunk.chunkIndex,
                        "metadata": chunk.metadata
                    }
                )
                points.append(point)

            # Upload points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"Inserted {len(points)} vectors into Qdrant")
        except Exception as e:
            print(f"Error inserting vectors: {e}")
            raise

    async def query_vectors(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query Qdrant for similar vectors
        """
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                with_payload=True
            )

            results = []
            for hit in search_result:
                result = {
                    "id": hit.id,
                    "content": hit.payload.get("content", ""),
                    "chapter_id": hit.payload.get("chapter_id", ""),
                    "chunk_index": hit.payload.get("chunk_index", 0),
                    "score": hit.score,
                    "metadata": hit.payload.get("metadata", {})
                }
                results.append(result)

            return results
        except Exception as e:
            print(f"Error querying vectors: {e}")
            raise

    async def delete_collection(self):
        """
        Delete the collection (useful for reindexing)
        """
        try:
            self.client.delete_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' deleted")
        except Exception as e:
            print(f"Error deleting collection: {e}")
            raise

# Global instance
qdrant_service = QdrantService()