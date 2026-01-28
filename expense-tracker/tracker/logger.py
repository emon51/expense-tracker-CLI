import logging
import os
from datetime import datetime


def setup_logger(name: str = "tracker", log_dir: str = "logs", log_file: str = "tracker.log") -> logging.Logger:
    """
    Set up and configure logger for the application.
    
    Args:
        name: Logger name
        log_dir: Directory for log files
        log_file: Log file name
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Avoid adding duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create file handler
    log_path = os.path.join(log_dir, log_file)
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Create console handler (for errors and warnings)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Create a default logger instance for the application
logger = setup_logger()


def log_command(command: str, args: dict = None):
    """
    Log a CLI command execution.
    
    Args:
        command: Command name (e.g., 'add', 'list', 'summary')
        args: Command arguments as dictionary
    """
    args_str = f" with args {args}" if args else ""
    logger.info(f"Command '{command}' executed{args_str}")


def log_validation_error(field: str, value: any, error: str):
    """
    Log a validation error.
    
    Args:
        field: Field name that failed validation
        value: Value that was validated
        error: Error message
    """
    logger.warning(f"Validation error - {field}='{value}': {error}")


def log_file_operation(operation: str, filepath: str, success: bool = True, error: str = None):
    """
    Log file read/write operations.
    
    Args:
        operation: Operation type ('read', 'write', 'delete')
        filepath: Path to the file
        success: Whether operation succeeded
        error: Error message if failed
    """
    if success:
        logger.info(f"File {operation} successful: {filepath}")
    else:
        logger.error(f"File {operation} failed: {filepath} - {error}")


def log_expense_added(expense_id: str, category: str, amount: float):
    """
    Log when an expense is added.
    
    Args:
        expense_id: ID of the added expense
        category: Category of expense
        amount: Amount of expense
    """
    logger.info(f"Expense added: {expense_id} | {category} | {amount}")


def log_expense_deleted(expense_id: str, success: bool = True):
    """
    Log when an expense is deleted.
    
    Args:
        expense_id: ID of the deleted expense
        success: Whether deletion succeeded
    """
    if success:
        logger.info(f"Expense deleted: {expense_id}")
    else:
        logger.warning(f"Expense deletion failed: {expense_id} not found")


def log_expense_updated(expense_id: str, success: bool = True):
    """
    Log when an expense is updated.
    
    Args:
        expense_id: ID of the updated expense
        success: Whether update succeeded
    """
    if success:
        logger.info(f"Expense updated: {expense_id}")
    else:
        logger.warning(f"Expense update failed: {expense_id} not found")


def log_error(error_type: str, message: str):
    """
    Log general errors.
    
    Args:
        error_type: Type of error
        message: Error message
    """
    logger.error(f"{error_type}: {message}")


def log_info(message: str):
    """
    Log general information.
    
    Args:
        message: Info message
    """
    logger.info(message)


def log_debug(message: str):
    """
    Log debug information.
    
    Args:
        message: Debug message
    """
    logger.debug(message)