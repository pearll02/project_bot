"""Application Configuration"""
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Google Gemini Configuration
    gemini_api_key: str
    gemini_model: str = "gemini-pro"
    embedding_api_key: Optional[str] = None  # Optional, uses Gemini for embeddings
    
    # Application Configuration
    app_name: str = "Document QA Chatbot"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # File Upload Configuration
    max_file_size: int = 52428800  # 50MB
    upload_dir: str = "data/uploads"
    
    # Vector Store Configuration
    vector_store_path: str = "data/vector_store"
    chunk_size: int = 500
    chunk_overlap: int = 100
    
    # RAG Configuration
    top_k_chunks: int = 5
    similarity_threshold: float = 0.5
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def upload_dir_path(self) -> Path:
        """Get upload directory as Path object"""
        path = Path(self.upload_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @property
    def vector_store_dir_path(self) -> Path:
        """Get vector store directory as Path object"""
        path = Path(self.vector_store_path)
        path.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
