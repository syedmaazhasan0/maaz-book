from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSelection(BaseModel):
    """
    Model representing a user's text selection
    """
    id: str
    sessionId: str
    text: str
    sourceUrl: str
    selectionStart: Optional[int] = None
    selectionEnd: Optional[int] = None
    createdAt: datetime