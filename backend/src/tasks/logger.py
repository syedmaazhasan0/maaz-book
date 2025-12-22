import os
import json
from datetime import datetime
from typing import Dict, Optional


class TaskLogger:
    """
    Handles logging for individual tasks, storing logs to a file and optionally to Weights & Biases (wandb).
    """

    def __init__(self, task_id: str, log_dir: str = "task_logs"):
        self.task_id = task_id
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f"{task_id}.log")

        # Initialize wandb if available and configured
        if os.getenv("WANDB_API_KEY") and os.getenv("WANDB_PROJECT"):
            try:
                import wandb
                wandb.init(project=os.getenv("WANDB_PROJECT"), name=f"task-{task_id}", reinit=True)
                self.wandb_run = wandb.run
            except ImportError:
                self.wandb_run = None
                print("Warning: wandb not installed. Logging to wandb disabled.")
        else:
            self.wandb_run = None
            print("Warning: WANDB_API_KEY or WANDB_PROJECT not set. Logging to wandb disabled.")

    def log(self, level: str, message: str, data: Optional[Dict] = None):
        """
        Logs a message with a given level, optionally including additional data.
        """
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] [{level.upper()}] {message}"
        if data:
            log_entry += f" Data: {json.dumps(data)}"

        # Log to file
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")

        # Log to console
        print(log_entry)

        # Log to wandb if enabled
        if self.wandb_run:
            log_data = {"timestamp": timestamp, "level": level, "message": message}
            if data:
                log_data.update(data)
            self.wandb_run.log({f"task_log/{level}": log_data})
