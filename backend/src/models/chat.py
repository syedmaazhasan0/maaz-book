from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatSession(BaseModel):
    """
    Model representing a chat session
    """
    id: str
    userId: Optional[str] = None
    createdAt: datetime
    lastActiveAt: datetime
    isActive: bool = True

class ChatMessage(BaseModel):
    """
    Model representing a chat message
    """
    id: str
    sessionId: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    contextUsed: Optional[str] = None