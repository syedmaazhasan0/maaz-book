import asyncio
from datetime import datetime
from typing import Any, Dict, Optional, Type

from src.models.task import Task, TaskData, TaskStatus
from src.tasks.base import BaseTask
# from backend.src.tasks.worker import TaskWorker # Will be implemented in T013


class TaskController:
    """
    Manages the lifecycle of tasks, distributing them to workers and tracking their status.
    """

    def __init__(self, task_registry: Dict[str, Type[BaseTask]]):
        self.task_registry = task_registry
        self.workers: Dict[str, Any] = {} # Type hint as Any for now, will be TaskWorker after T013
        self.tasks: Dict[str, Task] = {}
        self.task_queue: asyncio.Queue[TaskData] = asyncio.Queue()
        self.worker_update_queue: asyncio.Queue[Dict[str, Any]] = asyncio.Queue()
        self.lock = asyncio.Lock()  # For state management
        self.shutdown_event = asyncio.Event()

    async def register_worker(self, worker_id: str, worker_address: str) -> bool:
        """
        Registers a new worker with the controller.
        """
        async with self.lock:
            if worker_id not in self.workers:
                # Placeholder for TaskWorker creation until T013
                # worker = TaskWorker(worker_id, worker_address, self.task_queue, self.worker_update_queue, self.task_registry)
                self.workers[worker_id] = {"address": worker_address, "status": "registered"}
                print(f"Worker {worker_id} registered at {worker_address}")
                return True
            return False

    async def unregister_worker(self, worker_id: str) -> bool:
        """
        Unregisters a worker from the controller.
        """
        async with self.lock:
            if worker_id in self.workers:
                # await self.workers[worker_id].stop() # Uncomment after T013
                del self.workers[worker_id]
                print(f"Worker {worker_id} unregistered.")
                return True
            return False

    async def submit_task(self, task_data: TaskData) -> str:
        """
        Submits a new task for execution.
        """
        async with self.lock:
            if task_data.task_type not in self.task_registry:
                raise ValueError(f"Unknown task type: {task_data.task_type}")

            task = Task(
                task_id=task_data.task_id,
                task_type=task_data.task_type,
                params=task_data.params,
                status=TaskStatus.PENDING,
            )
            self.tasks[task.task_id] = task
            await self.task_queue.put(task_data)
            print(f"Task {task.task_id} submitted.")
            return task.task_id

    async def get_task_status(self, task_id: str) -> Optional[Task]:
        """
        Retrieves the current status of a task.
        """
        async with self.lock:
            return self.tasks.get(task_id)

    async def _update_task_status(self, update: Dict[str, Any]):
        """
        Internal method to update the status of a task based on worker feedback.
        """
        task_id = update["task_id"]
        status = update["status"]
        result = update.get("result")
        error = update.get("error")

        async with self.lock:
            task = self.tasks.get(task_id)
            if task:
                task.status = status
                task.updated_at = datetime.utcnow().isoformat()
                if result:
                    task.result = result
                if error:
                    task.history.append({"timestamp": task.updated_at, "event": "error", "details": error})
                task.history.append({"timestamp": task.updated_at, "event": "status_update", "status": status})
                print(f"Task {task_id} updated to {status}")
            else:
                print(f"Warning: Task {task_id} not found for status update.")

    async def _process_worker_updates(self):
        """
        Continuously processes status updates from workers.
        """
        while not self.shutdown_event.is_set():
            try:
                update = await asyncio.wait_for(self.worker_update_queue.get(), timeout=1.0)
                await self._update_task_status(update)
                self.worker_update_queue.task_done()
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(f"Error processing worker update: {e}")

    async def start(self):
        """
        Starts the TaskController, including background update processing.
        """
        print("TaskController starting...")
        asyncio.create_task(self._process_worker_updates())
        print("TaskController started.")

    async def stop(self):
        """
        Stops the TaskController and all registered workers.
        """
        print("TaskController stopping...")
        self.shutdown_event.set()
        await self.task_queue.join()
        for worker in self.workers.values(): # Will need to call worker.stop() after T013
            pass
        print("TaskController stopped.")
