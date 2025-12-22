import asyncio
import uuid
import time
import sys
import os

# Add the project root to sys.path
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.insert(0, project_root)

from backend.src.models.task import TaskData, TaskStatus
from backend.src.tasks.controller import TaskController
from backend.src.tasks.worker import TaskWorker
from backend.src.tasks.hello_task import HelloTask, DummyEnvClient # Import HelloTask and DummyEnvClient

async def test_task_execution():
    print("\n--- Starting Task Execution Test ---")

    # 1. Instantiate TaskController with HelloTask
    task_registry = {
        "hello_task": HelloTask
    }
    controller = TaskController(task_registry=task_registry)
    await controller.start()
    print("TaskController started.")

    # 2. Instantiate TaskWorker and start it
    worker_id = f"worker-{uuid.uuid4().hex[:8]}"
    controller_address = "http://localhost:8000" # Dummy address for worker registration
    dummy_env_client = DummyEnvClient() # Instantiate the dummy environment client

    worker = TaskWorker(
        worker_id=worker_id,
        controller_address=controller_address,
        task_queue=controller.task_queue, # Worker shares controller's task queue
        worker_update_queue=controller.worker_update_queue, # Worker shares controller's update queue
        task_registry=task_registry,
        environment_client=dummy_env_client # Pass the dummy environment client
    )
    await worker.start()
    print(f"TaskWorker {worker_id} started.")

    # Give some time for worker to potentially register (conceptual for now)
    await asyncio.sleep(0.1)

    # 3. Create a TaskData for HelloTask
    task_data = TaskData(
        task_type="hello_task",
        params={"message": "Greetings from the test script!"}
    )
    print(f"Submitting task: {task_data.task_id}")

    # 4. Submit the task to the TaskController
    submitted_task_id = await controller.submit_task(task_data)
    assert submitted_task_id == task_data.task_id
    print(f"Task {submitted_task_id} submitted to controller.")

    # 5. Poll the TaskController for the task status
    timeout = 5 # seconds
    start_time = time.time()
    while True:
        status = await controller.get_task_status(submitted_task_id)
        assert status is not None
        print(f"Task {submitted_task_id} status: {status.status}")

        if status.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            break
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Task {submitted_task_id} did not complete within {timeout} seconds.")
        await asyncio.sleep(0.5)

    # 6. Assert the result
    assert status.status == TaskStatus.COMPLETED
    assert status.result is not None
    assert "response" in status.result
    assert status.result["response"] == "Greetings from the test script!"
    print(f"Task {submitted_task_id} completed successfully with result: {status.result}")

    # 7. Stop the TaskWorker and TaskController
    await worker.stop()
    await controller.stop()
    print("TaskWorker and TaskController stopped.")

    print("--- Task Execution Test Completed Successfully ---")

if __name__ == "__main__":
    asyncio.run(test_task_execution())
