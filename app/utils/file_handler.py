"""File handling utilities"""
import os
import uuid
from pathlib import Path
from typing import Optional
from app.utils.logger import logger


ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.docx'}


def generate_document_id() -> str:
    """Generate a unique document ID"""
    return str(uuid.uuid4())


def validate_file_extension(filename: str) -> bool:
    """Validate if file has allowed extension"""
    extension = Path(filename).suffix.lower()
    return extension in ALLOWED_EXTENSIONS


def get_file_type(filename: str) -> str:
    """Get file type from filename"""
    extension = Path(filename).suffix.lower()
    if extension == '.pdf':
        return 'pdf'
    elif extension == '.txt':
        return 'txt'
    elif extension == '.docx':
        return 'docx'
    else:
        raise ValueError(f"Unsupported file type: {extension}")


def save_uploaded_file(file_content: bytes, filename: str, upload_dir: Path) -> str:
    """Save uploaded file and return full path"""
    try:
        # Sanitize filename
        safe_filename = Path(filename).name
        file_path = upload_dir / safe_filename
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        logger.info(f"File saved: {file_path}")
        return str(file_path)
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise


def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    return os.path.getsize(file_path)


def cleanup_file(file_path: str) -> bool:
    """Delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted: {file_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        return False
