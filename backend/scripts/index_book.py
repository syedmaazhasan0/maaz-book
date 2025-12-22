import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.content_ingestion_service import ContentIngestionService
from src.services.embedding_service import EmbeddingService
from src.services.qdrant_service import QdrantService


def index_book(book_path, book_id, title, author):
    """
    Index a book for RAG querying
    """
    print(f"Starting book indexing process...")

    # Initialize services
    ingestion_service = ContentIngestionService()
    embedding_service = EmbeddingService()
    qdrant_service = QdrantService()

    # Create collection first
    print("Creating Qdrant collection...")
    qdrant_service.create_collection(vector_size=1024)  # Cohere embed-english-v3.0 uses 1024 dimensions

    # Read book content
    print(f"Reading book from {book_path}...")
    with open(book_path, 'r', encoding='utf-8') as file:
        content = file.read()

    print(f"Processing book: {title} by {author}")
    print(f"Book content length: {len(content)} characters")

    # Create book with chunks
    book = ingestion_service.create_book_with_chunks(
        book_id=book_id,
        title=title,
        author=author,
        content=content
    )

    print(f"Book split into {len(book.chunks)} chunks")

    # Generate embeddings for all chunks
    print("Generating embeddings using Cohere...")
    embeddings = embedding_service.create_embeddings(book.chunks)

    # Prepare data for Qdrant
    vectors_to_upsert = []
    for i, chunk in enumerate(book.chunks):
        vectors_to_upsert.append({
            'id': i + 1,  # Use integer IDs for Qdrant
            'vector': embeddings[i],
            'payload': {
                'content': chunk.content,
                'book_id': chunk.book_id,
                'chunk_index': chunk.chunk_index,
                'chunk_id': chunk.id
            }
        })

    # Upsert vectors to Qdrant
    print("Upserting vectors to Qdrant...")
    qdrant_service.upsert_vectors(vectors_to_upsert)

    print(f"\n✓ Successfully indexed {len(vectors_to_upsert)} chunks for book: {title}")
    print(f"✓ Book ID: {book_id}")
    print(f"✓ You can now query the chatbot about this book!")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python index_book.py <book_path> <book_id> <title> <author>")
        sys.exit(1)

    book_path = sys.argv[1]
    book_id = sys.argv[2]
    title = sys.argv[3]
    author = sys.argv[4]

    index_book(book_path, book_id, title, author)
