# Replacing Book Content and Re-indexing Guide

This document explains how to replace the book content in the RAG system and re-index it for querying.

## Overview

The RAG (Retrieval-Augmented Generation) system works by:
1. Splitting book content into chunks
2. Generating embeddings for each chunk
3. Storing embeddings in Qdrant vector database
4. Retrieving relevant chunks based on user queries
5. Generating answers using the retrieved context

## Steps to Replace Book Content

### 1. Prepare Your Book Content

Your book content should be in plain text format. For best results:
- Ensure the text is clean and well-formatted
- Remove page numbers, headers, and other non-content elements
- Save as a `.txt` file

### 2. Use the Content Ingestion Service

The content ingestion service handles splitting and preparing the book content:

```python
from src.services.content_ingestion_service import ContentIngestionService
from src.services.embedding_service import EmbeddingService
from src.services.qdrant_service import QdrantService

# Initialize services
ingestion_service = ContentIngestionService()
embedding_service = EmbeddingService()
qdrant_service = QdrantService()

# Create book with chunks
with open('your-book.txt', 'r', encoding='utf-8') as file:
    book_content = file.read()

book = ingestion_service.create_book_with_chunks(
    book_id='your-book-id',
    title='Your Book Title',
    author='Author Name',
    content=book_content
)

# Generate embeddings for all chunks
embeddings = embedding_service.create_embeddings(book.chunks)

# Prepare data for Qdrant
vectors_to_upsert = []
for i, chunk in enumerate(book.chunks):
    vectors_to_upsert.append({
        'id': chunk.id,
        'vector': embeddings[i],
        'payload': {
            'content': chunk.content,
            'book_id': chunk.book_id,
            'chunk_index': chunk.chunk_index,
            'chunk_id': chunk.id
        }
    })

# Upsert vectors to Qdrant
qdrant_service.upsert_vectors(vectors_to_upsert)
```

### 3. Alternative: Using a Script

You can create a script to automate the process:

```python
# scripts/index_book.py
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
    # Initialize services
    ingestion_service = ContentIngestionService()
    embedding_service = EmbeddingService()
    qdrant_service = QdrantService()
    
    # Read book content
    with open(book_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    print(f"Processing book: {title} by {author}")
    
    # Create book with chunks
    book = ingestion_service.create_book_with_chunks(
        book_id=book_id,
        title=title,
        author=author,
        content=content
    )
    
    print(f"Book split into {len(book.chunks)} chunks")
    
    # Generate embeddings for all chunks
    print("Generating embeddings...")
    embeddings = embedding_service.create_embeddings(book.chunks)
    
    # Prepare data for Qdrant
    vectors_to_upsert = []
    for i, chunk in enumerate(book.chunks):
        vectors_to_upsert.append({
            'id': chunk.id,
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
    
    print(f"Successfully indexed {len(vectors_to_upsert)} chunks for book: {title}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python index_book.py <book_path> <book_id> <title> <author>")
        sys.exit(1)
    
    book_path = sys.argv[1]
    book_id = sys.argv[2]
    title = sys.argv[3]
    author = sys.argv[4]
    
    index_book(book_path, book_id, title, author)
```

Run the script:
```bash
python scripts/index_book.py path/to/your/book.txt my-book-id "My Book Title" "Author Name"
```

### 4. Verification

After indexing, you can verify the book is properly indexed by querying the system:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this book about?",
    "book_id": "my-book-id"
  }'
```

## Best Practices

1. **Chunk Size**: The default chunk size is 1000 characters with 100-character overlap. Adjust based on your content type.

2. **Content Quality**: Clean, well-structured text will produce better query results.

3. **Book IDs**: Use unique, descriptive book IDs to avoid conflicts.

4. **Testing**: Always test with sample queries after indexing to ensure the content is properly retrievable.

5. **Performance**: For large books, indexing may take some time. Consider running the indexing process during off-peak hours.

## Troubleshooting

- If queries return no results, verify the book was properly indexed in Qdrant
- If responses seem unrelated to the question, consider adjusting the chunk size or overlap
- If you encounter API rate limits, consider implementing batching during the indexing process