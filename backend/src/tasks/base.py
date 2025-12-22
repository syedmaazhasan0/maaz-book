from abc import ABC, abstractmethod
from typing import Any

from src.models.task import TaskData
from src.tasks.logger import TaskLogger


class BaseEnvClient(ABC):
    """
    Base class for environment clients.
    An environment client interacts with the external environment where tasks are performed.
    """

    @abstractmethod
    def get_state(self) -> Any:
        """
        Retrieves the current state of the environment.
        """
        pass

    @abstractmethod
    def update_state(self, action: Any) -> Any:
        """
        Updates the state of the environment based on a given action.
        """
        pass


class BaseTask(ABC):
    """
    Base class for all executable tasks.
    Each task operates on TaskData and interacts with an Environment Client.
    """

    def __init__(self, task_data: TaskData, environment_client: BaseEnvClient):
        self.task_data = task_data
        self.environment_client = environment_client
        self.logger = TaskLogger(task_data.task_id)

    @abstractmethod
    def execute(self) -> Any:
        """
        Abstract method to be implemented by concrete task classes.
        Contains the core logic for executing the task.
        """
        pass

    def log_progress(self, message: str, level: str = "info"):
        """
        Logs progress or significant events during task execution.
        """
        self.logger.log(level, message)
