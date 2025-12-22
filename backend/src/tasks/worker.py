import asyncio
import traceback
from typing import Any, Dict, Type

from backend.src.models.task import TaskData, TaskStatus
from backend.src.tasks.base import BaseTask, BaseEnvClient # Import BaseEnvClient
from collections import deque


class TaskWorker:
    """
    A worker process that executes tasks received from the TaskController.
    """

    def __init__(self, worker_id: str, controller_address: str,
                 task_queue: asyncio.Queue[TaskData],
                 worker_update_queue: asyncio.Queue[Dict[str, Any]],
                 task_registry: Dict[str, Type[BaseTask]],
                 environment_client: BaseEnvClient # Added environment_client
                 ):
        self.worker_id = worker_id
        self.controller_address = controller_address
        self.task_queue = task_queue
        self.worker_update_queue = worker_update_queue
        self.task_registry = task_registry
        self.environment_client = environment_client # Store environment_client
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.shutdown_event = asyncio.Event()

    async def _execute_task(self, task_data: TaskData):
        """
        Executes a single task.
        """
        task_type = task_data.task_type
        task_id = task_data.task_id

        try:
            # Pass environment_client to the task instance
            task_instance = self.task_registry[task_type](task_data, self.environment_client)
            await self.worker_update_queue.put({
                "task_id": task_id,
                "status": TaskStatus.RUNNING,
                "worker_id": self.worker_id
            })
            result = await task_instance.execute()
            await self.worker_update_queue.put({
                "task_id": task_id,
                "status": TaskStatus.COMPLETED,
                "result": result,
                "worker_id": self.worker_id
            })
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(f"Error executing task {task_id}: {e}\n{traceback_str}")
            await self.worker_update_queue.put({
                "task_id": task_id,
                "status": TaskStatus.FAILED,
                "error": str(e),
                "traceback": traceback_str,
                "worker_id": self.worker_id
            })
        finally:
            del self.running_tasks[task_id]

    async def _process_tasks(self):
        """
        Continuously pulls and processes tasks from the queue.
        """
        while not self.shutdown_event.is_set():
            try:
                task_data = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                if task_data.task_id not in self.running_tasks:
                    print(f"Worker {self.worker_id} starting task {task_data.task_id}")
                    self.running_tasks[task_data.task_id] = asyncio.create_task(self._execute_task(task_data))
                self.task_queue.task_done()
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(f"Worker {self.worker_id} error processing task: {e}")

    async def start(self):
        """
        Starts the TaskWorker, including task processing.
        """
        print(f"TaskWorker {self.worker_id} starting...")
        # In a real scenario, this would be an HTTP POST to controller_address/register_worker
        # For now, it's a conceptual registration.
        print(f"TaskWorker {self.worker_id} registering with controller at {self.controller_address}")

        asyncio.create_task(self._process_tasks())
        print(f"TaskWorker {self.worker_id} started.")

    async def stop(self):
        """
        Stops the TaskWorker and cancels all running tasks.
        """
        print(f"TaskWorker {self.worker_id} stopping...")
        self.shutdown_event.set()
        for task in self.running_tasks.values():
            task.cancel()
        await asyncio.gather(*self.running_tasks.values(), return_exceptions=True)
        print(f"TaskWorker {self.worker_id} stopped.")
