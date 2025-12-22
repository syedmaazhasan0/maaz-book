from typing import Any, Dict, Optional

from src.models.task import Task, TaskData
from src.tasks.controller import TaskController


class TaskHandler:
    """
    Handles incoming requests related to tasks, delegating to the TaskController.
    This acts as an intermediary between the API layer and the core task logic.
    """

    def __init__(self, task_controller: TaskController):
        self.task_controller = task_controller

    async def handle_submit_task(self, task_type: str, params: Dict[str, Any]) -> Optional[Task]:
        """
        Submits a new task through the controller and returns its initial status.
        """
        task_data = TaskData(task_type=task_type, params=params)
        task_id = await self.task_controller.submit_task(task_data)
        return await self.task_controller.get_task_status(task_id)

    async def handle_get_task_status(self, task_id: str) -> Optional[Task]:
        """
        Retrieves the current status of a specific task.
        """
        return await self.task_controller.get_task_status(task_id)

    async def handle_register_worker(self, worker_id: str, worker_address: str) -> bool:
        """
        Registers a worker with the task controller.
        """
        return await self.task_controller.register_worker(worker_id, worker_address)

    async def handle_unregister_worker(self, worker_id: str) -> bool:
        """
        Unregisters a worker from the task controller.
        """
        return await self.task_controller.unregister_worker(worker_id)
