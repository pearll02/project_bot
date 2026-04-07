"""Document upload and processing service"""
from pathlib import Path
from app.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.utils.logger import logger
from app.utils.document_parser import extract_text_from_file
from app.utils.text_processor import chunk_text, clean_text
from app.utils.file_handler import (
    generate_document_id,
    get_file_type,
    validate_file_extension
)


class DocumentService:
    """Service for uploading and processing documents"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.embedding_service = EmbeddingService()
    
    def process_document(
        self,
        file_path: str,
        filename: str
    ) -> dict:
        """
        Process uploaded document and store in vector DB
        
        Args:
            file_path: Path to the uploaded file
            filename: Original filename
        
        Returns:
            Dictionary with processing results
        """
        try:
            # Generate document ID
            document_id = generate_document_id()
            
            # Get file type
            if not validate_file_extension(filename):
                raise ValueError(f"Unsupported file type: {filename}")
            
            file_type = get_file_type(filename)
            logger.info(f"Processing {file_type} document: {filename}")
            
            # Extract text from document
            text = extract_text_from_file(file_path, file_type)
            
            # Clean text
            text = clean_text(text)
            logger.info(f"Extracted {len(text)} characters from document")
            
            # Chunk text
            chunks = chunk_text(
                text,
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap
            )
            
            if not chunks:
                raise ValueError("No text chunks extracted from document")
            
            logger.info(f"Created {len(chunks)} chunks from document")
            
            # Generate embeddings
            embeddings = self.embedding_service.generate_embeddings(chunks)
            
            # Store in vector DB
            chunks_count = self.vector_store.add_documents(
                embeddings=embeddings,
                document_id=document_id,
                chunks=chunks,
                filename=filename
            )
            
            # Save vector store
            self.vector_store.save(str(settings.vector_store_dir_path))
            
            logger.info(f"Successfully processed document: {document_id}")
            
            return {
                "document_id": document_id,
                "filename": filename,
                "file_type": file_type,
                "chunks_count": chunks_count,
                "text_length": len(text)
            }
        
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise
    
    def get_document_info(self, document_id: str) -> dict:
        """Get information about a stored document"""
        chunks = self.vector_store.get_documents(document_id)
        
        if not chunks:
            return None
        
        # Get filename from first chunk metadata
        for metadata in self.vector_store.metadata.values():
            if metadata['document_id'] == document_id:
                return {
                    "document_id": document_id,
                    "filename": metadata['filename'],
                    "chunks_count": len(chunks)
                }
        
        return None
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document from storage"""
        try:
            self.vector_store.delete_document(document_id)
            self.vector_store.save(str(settings.vector_store_dir_path))
            logger.info(f"Deleted document: {document_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False
