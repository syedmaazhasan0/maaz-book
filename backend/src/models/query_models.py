from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    question: str
    book_id: str
    selected_text: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    mode_used: str  # "full_book" or "selected_text"