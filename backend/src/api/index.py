from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
import datetime
from src.services.qdrant_service import qdrant_service
from src.services.embedding_service import embedding_service
from src.utils.chunker import chunker

router = APIRouter()

# Request and response models
class Chapter(BaseModel):
    id: str
    title: str
    content: str

class IndexRequest(BaseModel):
    chapters: List[Chapter]
    forceReindex: bool = False

class IndexResponse(BaseModel):
    status: str
    indexedCount: int
    message: str

@router.post("/index", response_model=IndexResponse)
async def index_content(request: IndexRequest):
    """
    Index book content for RAG retrieval
    """
    try:
        # Validate input
        if not request.chapters:
            raise HTTPException(status_code=400, detail="No chapters provided for indexing")

        if any(not chapter.id or not chapter.title or not chapter.content for chapter in request.chapters):
            raise HTTPException(status_code=400, detail="All chapters must have id, title, and content")

        # Create collection if it doesn't exist
        await qdrant_service.create_collection()

        # Process each chapter
        total_chunks = 0
        for chapter in request.chapters:
            # Chunk the chapter content
            chunks = chunker.chunk_text(chapter.content, chapter.id)

            # Generate embeddings for each chunk
            for chunk in chunks:
                chunk.embedding = await embedding_service.create_embedding(chunk.content)

            # Insert chunks into Qdrant
            await qdrant_service.insert_vectors(chunks)
            total_chunks += len(chunks)

        return IndexResponse(
            status="success",
            indexedCount=total_chunks,
            message=f"Successfully indexed {len(request.chapters)} chapters ({total_chunks} chunks)"
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logging.error(f"Error indexing content: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during indexing")

@router.get("/index/status")
async def get_index_status():
    """
    Get the status of the indexing process
    """
    try:
        # This is a placeholder implementation
        return {"status": "ready", "indexed_chunks": 0, "last_updated": "never"}
    except Exception as e:
        logging.error(f"Error getting index status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error getting index status")