from typing import Any
from src.tasks.base import BaseTask, BaseEnvClient
from src.models.task import TaskData

class DummyEnvClient(BaseEnvClient):
    """
    A dummy environment client for testing purposes.
    """
    def get_state(self) -> Any:
        """
        Returns a fixed dummy state.
        """
        return "Dummy State"
    
    def update_state(self, action: Any) -> Any:
        """
        Prints the received action and returns a dummy response.
        """
        print(f"Dummy Env received action: {action}")
        return f"Dummy response to {action}"

class HelloTask(BaseTask):
    """
    A simple task that logs a message and interacts with a dummy environment.
    """
    def __init__(self, task_data: TaskData, environment_client: BaseEnvClient):
        super().__init__(task_data, environment_client)

    async def execute(self) -> Any:
        """
        Executes the 'HelloTask', logs a message, and simulates environment interaction.
        """
        message = self.task_data.params.get("message", "Hello from HelloTask!")
        self.log_progress(f"Executing HelloTask with message: {message}")
        # Simulate some work with the environment
        state = self.environment_client.get_state()
        self.log_progress(f"Environment initial state: {state}")
        self.environment_client.update_state(f"Processed: {message}")
        return {"response": message, "worker_id": "dummy_worker_id"}
