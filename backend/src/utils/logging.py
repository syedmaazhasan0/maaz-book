import logging
from datetime import datetime
import os
from logging.handlers import RotatingFileHandler


def setup_logging():
    """
    Set up comprehensive logging for the application
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create a file handler with rotation
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    
    # Create a formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def log_api_call(endpoint: str, method: str, user_id: str = None, details: dict = None):
    """
    Log an API call with relevant details
    """
    logger = logging.getLogger(__name__)
    logger.info(f"API_CALL: {method} {endpoint} | User: {user_id} | Details: {details}")


def log_error(error: Exception, context: str = ""):
    """
    Log an error with context
    """
    logger = logging.getLogger(__name__)
    logger.error(f"ERROR in {context}: {str(error)}", exc_info=True)


def log_performance(operation: str, duration: float, details: dict = None):
    """
    Log performance metrics for an operation
    """
    logger = logging.getLogger(__name__)
    logger.info(f"PERFORMANCE: {operation} took {duration:.2f}s | Details: {details}")


# Initialize logging when module is imported
app_logger = setup_logging()