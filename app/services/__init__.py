"""Services for document processing, embeddings, and RAG"""
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.document_service import DocumentService
from app.services.rag_service import RAGService
from app.config import settings
from app.utils.logger import logger

# Global service instances (shared across all routers)
_embedding_service = None
_vector_store = None
_document_service = None
_rag_service = None


def initialize_services():
    """Initialize all services once"""
    global _embedding_service, _vector_store, _document_service, _rag_service
    
    if _embedding_service is None:
        logger.info("Initializing services...")
        
        _embedding_service = EmbeddingService()
        _vector_store = VectorStore(embedding_dim=_embedding_service.get_embedding_dimension())
        _document_service = DocumentService(_vector_store)
        _rag_service = RAGService(_vector_store)
        
        # Load existing vector store if available
        try:
            _vector_store.load(str(settings.vector_store_dir_path))
            logger.info("Loaded existing vector store")
        except Exception as e:
            logger.debug(f"Could not load existing vector store: {str(e)}")
    
    return _embedding_service, _vector_store, _document_service, _rag_service


def get_embedding_service() -> EmbeddingService:
    """Get embedding service instance"""
    embedding_service, _, _, _ = initialize_services()
    return embedding_service


def get_vector_store() -> VectorStore:
    """Get vector store instance"""
    _, vector_store, _, _ = initialize_services()
    return vector_store


def get_document_service() -> DocumentService:
    """Get document service instance"""
    _, _, document_service, _ = initialize_services()
    return document_service


def get_rag_service() -> RAGService:
    """Get RAG service instance"""
    _, _, _, rag_service = initialize_services()
    return rag_service
