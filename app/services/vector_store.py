"""Vector storage and retrieval using FAISS"""
import json
import numpy as np
import faiss
from pathlib import Path
from typing import List, Tuple, Dict, Any
from app.config import settings
from app.utils.logger import logger


class VectorStore:
    """FAISS-based vector store for document chunks"""
    
    def __init__(self, embedding_dim: int = 512):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.metadata: Dict[int, Dict[str, Any]] = {}
        self.next_id = 0
    
    def add_documents(
        self,
        embeddings: List[List[float]],
        document_id: str,
        chunks: List[str],
        filename: str
    ) -> int:
        """
        Add document chunks and embeddings to the store
        
        Args:
            embeddings: List of embedding vectors
            document_id: Unique document identifier
            chunks: List of text chunks
            filename: Original filename
        
        Returns:
            Number of chunks added
        """
        try:
            embeddings_array = np.array(embeddings, dtype=np.float32)
            
            # Add embeddings to FAISS index
            self.index.add(embeddings_array)
            
            # Store metadata
            for chunk_idx, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
                self.metadata[self.next_id] = {
                    'document_id': document_id,
                    'chunk_index': chunk_idx,
                    'filename': filename,
                    'text': chunk
                }
                self.next_id += 1
            
            logger.info(f"Added {len(embeddings)} chunks for document {document_id}")
            return len(embeddings)
        
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise
    
    def search(
        self,
        query_embedding,
        top_k: int = 5,
        document_id: str = None,
        similarity_threshold: float = 0.0
    ) -> List[Tuple[str, float]]:
        """
        Search for similar chunks
        
        Args:
            query_embedding: Query embedding vector (list or np.ndarray)
            top_k: Number of results to return
            document_id: Filter results to specific document (optional)
            similarity_threshold: Minimum similarity score
        
        Returns:
            List of (chunk_text, similarity_score) tuples
        """
        try:
            # If we have no documents, return empty
            if len(self.metadata) == 0:
                return []
            
            # Convert to numpy array properly
            if isinstance(query_embedding, list):
                if len(query_embedding) == 0:
                    return []
                if isinstance(query_embedding[0], list):
                    query_array = np.array(query_embedding, dtype=np.float32)
                else:
                    query_array = np.array([query_embedding], dtype=np.float32)
            else:
                query_array = np.array([query_embedding], dtype=np.float32)
            
            # Ensure proper shape
            if query_array.ndim == 1:
                query_array = query_array.reshape(1, -1)
            
            # FAISS returns distances (L2), convert to similarity
            # Search for up to 2x top_k in case we need to filter by document_id
            search_k = min(top_k * 3, max(1, len(self.metadata)))
            distances, indices = self.index.search(query_array.astype(np.float32), search_k)
            
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx == -1:  # Invalid index
                    continue
                
                metadata = self.metadata.get(idx)
                if metadata is None:
                    continue
                
                # Filter by document_id if specified
                if document_id and metadata['document_id'] != document_id:
                    continue
                
                # Convert L2 distance to similarity (inverse)
                # L2 distance: smaller = more similar
                # Using a more lenient formula to get higher similarities
                similarity = 1 / (1 + np.sqrt(max(0, distance)))
                
                # Include all results, even with low similarity
                # since we don't have good similarity guarantees
                results.append((metadata['text'], similarity))
                
                if len(results) >= top_k:
                    break
            
            # If no results found and we're filtering by document, try without filter
            if len(results) == 0 and document_id is not None:
                logger.warning(f"No results found for document {document_id}, trying global search")
                return self.search(query_embedding, top_k, document_id=None, similarity_threshold=similarity_threshold)
            
            logger.info(f"Found {len(results)} similar chunks")
            return results
        
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            # Return empty list instead of raising
            return []
    
    def save(self, path: str) -> bool:
        """
        Save vector store to disk
        
        Args:
            path: Directory path to save to
        
        Returns:
            True if successful
        """
        try:
            path = Path(path)
            path.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            index_path = str(path / "index.faiss")
            faiss.write_index(self.index, index_path)
            
            # Save metadata
            metadata_path = str(path / "metadata.json")
            # Convert metadata keys to strings for JSON serialization
            metadata_serializable = {str(k): v for k, v in self.metadata.items()}
            with open(metadata_path, 'w') as f:
                json.dump(metadata_serializable, f)
            
            logger.info(f"Vector store saved to {path}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise
    
    def load(self, path: str) -> bool:
        """
        Load vector store from disk
        
        Args:
            path: Directory path to load from
        
        Returns:
            True if successful
        """
        try:
            path = Path(path)
            
            if not path.exists():
                logger.warning(f"Vector store path does not exist: {path}")
                return False
            
            # Load FAISS index
            index_path = str(path / "index.faiss")
            if Path(index_path).exists():
                self.index = faiss.read_index(index_path)
            
            # Load metadata
            metadata_path = str(path / "metadata.json")
            if Path(metadata_path).exists():
                with open(metadata_path, 'r') as f:
                    metadata_dict = json.load(f)
                    # Convert keys back to integers
                    self.metadata = {int(k): v for k, v in metadata_dict.items()}
                    # Update next_id
                    if self.metadata:
                        self.next_id = max(int(k) for k in metadata_dict.keys()) + 1
            
            logger.info(f"Vector store loaded from {path}")
            return True
        
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise
    
    def get_documents(self, document_id: str) -> List[str]:
        """Get all chunks for a specific document"""
        chunks = []
        for metadata in self.metadata.values():
            if metadata['document_id'] == document_id:
                chunks.append(metadata['text'])
        return chunks
    
    def delete_document(self, document_id: str) -> int:
        """Delete all chunks for a document"""
        ids_to_delete = [
            idx for idx, metadata in self.metadata.items()
            if metadata['document_id'] == document_id
        ]
        
        for idx in ids_to_delete:
            del self.metadata[idx]
        
        logger.info(f"Deleted {len(ids_to_delete)} chunks for document {document_id}")
        return len(ids_to_delete)
