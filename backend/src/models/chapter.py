from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class BookChapter(BaseModel):
    """
    Model representing a book chapter
    """
    id: str
    title: str
    content: str
    wordCount: Optional[int] = None
    position: int
    tags: List[str] = []
    createdAt: datetime
    updatedAt: datetime

class ContentChunk(BaseModel):
    """
    Model representing a chunk of content for embedding
    """
    id: str
    content: str
    chapterId: str
    chunkIndex: int
    embedding: Optional[List[float]] = None  # Vector embedding
    metadata: dict = {}