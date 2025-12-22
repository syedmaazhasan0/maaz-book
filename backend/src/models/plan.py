from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4

class Plan(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: Optional[str] = None
    steps: List[Dict] = []  # Each step could be a dictionary representing a task or action
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
