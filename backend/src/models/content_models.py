from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ContentChunk(BaseModel):
    id: str
    content: str
    book_id: str
    chunk_index: int
    vector_id: Optional[str] = None


class BookContent(BaseModel):
    id: str
    title: str
    author: str
    content: str
    chunks: List[ContentChunk] = []
    metadata: dict = {}