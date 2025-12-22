from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class TaskData:
    task_id: str
    task_type: str
    params: dict

    def __init__(self, task_type: str, params: dict, task_id: Optional[str] = None):
        if task_id is None:
            task_id = str(uuid4())
        self.task_id = task_id
        self.task_type = task_type
        self.params = params


class Task(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    task_id: str
    task_type: str
    params: dict
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    history: List[Dict] = []
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
