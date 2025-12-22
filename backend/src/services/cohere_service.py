import cohere
from typing import List
from src.config import settings


class CohereClient:
    def __init__(self):
        self.client = cohere.Client(api_key=settings.cohere_api_key)
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """
        Generate a response using Cohere's chat model
        """
        try:
            # Create the full prompt with context
            full_prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"
            
            response = self.client.generate(
                model='command-r-plus',  # Using Cohere's powerful model
                prompt=full_prompt,
                max_tokens=500,
                temperature=0.3
            )
            
            return response.generations[0].text.strip()
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for the provided texts using Cohere
        """
        try:
            response = self.client.embed(
                texts=texts,
                model="embed-english-v3.0",  # Cohere's latest embedding model
                input_type="search_document"
            )
            
            return response.embeddings
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")