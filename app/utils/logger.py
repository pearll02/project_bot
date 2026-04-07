"""Logging configuration module"""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(log_dir: str = "logs", level=logging.INFO) -> logging.Logger:
    """
    Setup logging configuration with both file and console handlers
    
    Args:
        log_dir: Directory to store log files
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("app")
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.hasHandlers():
        return logger
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Initialize and export logger
logger = setup_logging()
