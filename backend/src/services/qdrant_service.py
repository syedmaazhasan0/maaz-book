from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
from src.config import settings


class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False  # Using REST API
        )
        self.collection_name = "book_collection"
        
    def create_collection(self, vector_size: int = 1024):
        """
        Create a Qdrant collection for storing content embeddings
        """
        try:
            # Check if collection already exists
            self.client.get_collection(collection_name=self.collection_name)
            print(f"Collection {self.collection_name} already exists")
        except:
            # Create the collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created collection {self.collection_name}")
    
    def upsert_vectors(self, vectors: List[Dict[str, Any]]):
        """
        Upsert vectors to the collection
        Each vector dict should have: id, vector, payload
        """
        try:
            points = []
            for item in vectors:
                points.append(models.PointStruct(
                    id=item["id"],
                    vector=item["vector"],
                    payload=item["payload"]
                ))
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
        except Exception as e:
            raise Exception(f"Error upserting vectors: {str(e)}")
    
    def search_similar(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the collection
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k
            )
            
            return [
                {
                    "id": result.id,
                    "payload": result.payload,
                    "score": result.score
                }
                for result in results
            ]
        except Exception as e:
            raise Exception(f"Error searching vectors: {str(e)}")