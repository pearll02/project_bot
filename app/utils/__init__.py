"""Logging configuration"""
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration"""
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("doc_qa_api")
    logger.setLevel(getattr(logging, log_level))
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, log_level))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Create global logger instance
logger = setup_logging()
