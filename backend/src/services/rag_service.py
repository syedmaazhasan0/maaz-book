import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
from backend.src.services.embedding_service import embedding_service
from backend.src.services.qdrant_service import qdrant_service
from backend.src.services.retrieval_service import retrieval_service
from backend.src.models.chapter import ContentChunk

# Load environment variables
load_dotenv()

class RAGService:
    """
    Service for implementing Retrieval-Augmented Generation functionality
    """

    def __init__(self):
        # Initialize OpenAI client with API key from environment
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def generate_response(self, query: str, context: str) -> str:
        """
        Generate a response using OpenAI based on query and context
        """
        try:
            prompt = f"""
            Context information is below.
            ---------------------
            {context}
            ---------------------
            Given the context information and not prior knowledge, answer the query.
            Query: {query}
            Answer:
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can also use gpt-4 if available
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            raise

    async def retrieve_context(self, query: str, top_k: int = 5) -> str:
        """
        Retrieve relevant context from Qdrant based on the query
        """
        try:
            # Use the retrieval service to get relevant documents
            search_results = await retrieval_service.retrieve_relevant_documents(query, top_k)

            # Combine the content from results
            context_parts = []
            for result in search_results:
                context_parts.append(result["content"])

            return "\n\n".join(context_parts)
        except Exception as e:
            print(f"Error retrieving context: {e}")
            raise

    async def process_query_with_selected_text(self, query: str, selected_text: str) -> str:
        """
        Process a query using only the selected text as context
        """
        try:
            prompt = f"""
            Using only the following text, answer the question.
            Text: {selected_text}
            Question: {query}
            Answer:
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based only on the provided text."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error processing query with selected text: {e}")
            raise

    async def process_full_rag_query(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Process a full RAG query: retrieve context and generate response
        """
        try:
            # Retrieve context from vector store
            context = await self.retrieve_context(query, top_k)

            # Generate response using the context
            response = await self.generate_response(query, context)

            # For now, return a simple structure
            # In a real implementation, you'd want to return more detailed information
            return {
                "response": response,
                "context_used": context[:200] + "..." if len(context) > 200 else context,  # Truncate for display
                "sources": ["Retrieved from book content"]  # In a real implementation, this would contain actual sources
            }
        except Exception as e:
            print(f"Error processing full RAG query: {e}")
            raise

# Global instance
rag_service = RAGService()