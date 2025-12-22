from typing import Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Body

from src.models.task import Task, TaskData
from src.tasks.controller import TaskController
from src.tasks.handler import TaskHandler
from src.tasks.hello_task import HelloTask # Import the dummy task


router = APIRouter()

# --- Dependency Injection ---
# In a real application, these would be managed by a proper DI framework
# or instantiated in the main app and passed around.
# For simplicity, we create singletons here.

_task_controller: Optional[TaskController] = None
_task_handler: Optional[TaskHandler] = None


async def get_task_controller() -> TaskController:
    global _task_controller
    if _task_controller is None:
        # Register available task types here
        task_registry = {
            "hello_task": HelloTask
        }
        _task_controller = TaskController(task_registry=task_registry)
        await _task_controller.start() # Start the controller when it's first requested
    return _task_controller


async def get_task_handler(controller: TaskController = Depends(get_task_controller)) -> TaskHandler:
    global _task_handler
    if _task_handler is None:
        _task_handler = TaskHandler(task_controller=controller)
    return _task_handler


# --- API Endpoints ---

@router.post("/tasks/", response_model=Task)
async def submit_task_endpoint(
    task_request: TaskData,
    handler: TaskHandler = Depends(get_task_handler)
):
    """
    Submits a new task for execution.
    """
    task = await handler.handle_submit_task(task_request.task_type, task_request.params)
    if task:
        return task
    raise HTTPException(status_code=400, detail="Task submission failed")


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task_status_endpoint(
    task_id: str,
    handler: TaskHandler = Depends(get_task_handler)
):
    """
    Retrieves the current status of a submitted task.
    """
    task = await handler.handle_get_task_status(task_id)
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/workers/register", response_model=bool)
async def register_worker_endpoint(
    worker_id: str = Body(..., embed=True),
    worker_address: str = Body(..., embed=True),
    handler: TaskHandler = Depends(get_task_handler)
):
    """
    Registers a worker with the task controller.
    """
    success = await handler.handle_register_worker(worker_id, worker_address)
    return success


@router.post("/workers/unregister", response_model=bool)
async def unregister_worker_endpoint(
    worker_id: str = Body(..., embed=True),
    handler: TaskHandler = Depends(get_task_handler)
):
    """
    Unregisters a worker from the task controller.
    """
    success = await handler.handle_unregister_worker(worker_id)
    return success
