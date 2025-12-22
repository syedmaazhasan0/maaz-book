import httpx
from typing import Any, Dict, Optional

from backend.src.models.task import Task


class TaskClient:
    """
    Client for interacting with the TaskController API.
    """

    def __init__(self, controller_url: str):
        self.controller_url = controller_url

    async def submit_task(self, task_type: str, params: Dict[str, Any]) -> Task:
        """
        Submits a new task to the TaskController.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.controller_url}/tasks/", json={
                "task_type": task_type,
                "params": params
            })
            response.raise_for_status()  # Raises an exception for HTTP errors
            return Task(**response.json())

    async def get_task_status(self, task_id: str) -> Optional[Task]:
        """
        Retrieves the status of a specific task from the TaskController.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.controller_url}/tasks/{task_id}")
            response.raise_for_status()  # Raises an exception for HTTP errors
            return Task(**response.json())
