"""Embedding Service using TF-IDF (No External API Required)"""
import numpy as np
from typing import List, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from app.utils.logger import logger


class EmbeddingService:
    """
    Local embedding service using TF-IDF with fallback to simple semantic matching.
    No API calls required - works offline.
    """
    
    def __init__(self, embedding_dim: int = 384):
        """
        Initialize embedding service
        
        Args:
            embedding_dim: Desired embedding dimension (default: 384)
        """
        self.embedding_dim = embedding_dim
        self.vectorizer = None
        self.fitted_texts = []
        self._is_fitted = False
        logger.info(f"Initialized embedding service with dimension {embedding_dim}")
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for texts using TF-IDF
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            2D numpy array of embeddings (n_texts, embedding_dim)
        """
        if not texts:
            return np.array([])
        
        try:
            # Always generate embeddings, even if vectorizer isn't fitted
            embeddings = self._create_embeddings(texts)
            return embeddings.astype(np.float32)
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            # Return simple word count embeddings as fallback
            return self._fallback_embeddings(texts)
    
    def _create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings using TF-IDF"""
        # Create vectorizer if needed
        if self.vectorizer is None:
            self.vectorizer = TfidfVectorizer(
                max_features=min(self.embedding_dim, 300),
                lowercase=True,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1,
                max_df=1.0
            )
        
        # Fit on all texts if not already fitted
        if not self._is_fitted:
            try:
                self.vectorizer.fit(texts)
                self.fitted_texts = texts.copy()
                self._is_fitted = True
            except:
                # Fallback fit
                self.vectorizer.fit(['default text'])
                self._is_fitted = True
        
        # Transform texts
        embeddings = self.vectorizer.transform(texts).toarray()
        
        # Pad to embedding_dim
        if embeddings.shape[1] < self.embedding_dim:
            padding = np.zeros((embeddings.shape[0], self.embedding_dim - embeddings.shape[1]))
            embeddings = np.hstack([embeddings, padding])
        elif embeddings.shape[1] > self.embedding_dim:
            embeddings = embeddings[:, :self.embedding_dim]
        
        return embeddings
    
    def _fallback_embeddings(self, texts: List[str]) -> np.ndarray:
        """Fallback embedding using simple word matching"""
        embeddings = []
        
        for text in texts:
            # Simple embedding: word presence
            embedding = np.zeros(self.embedding_dim)
            words = text.lower().split()
            
            for i, word in enumerate(words[:self.embedding_dim]):
                # Simple: word length as value
                embedding[i] = np.sqrt(len(word)) / 10.0
            
            embeddings.append(embedding)
        
        return np.array(embeddings, dtype=np.float32)
    
    def generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single query
        
        Args:
            text: Query text
            
        Returns:
            List of floats representing the embedding
        """
        embeddings = self.generate_embeddings([text])
        if len(embeddings) > 0:
            return embeddings[0].tolist()
        return [0.0] * self.embedding_dim
    
    def get_embedding_dimension(self) -> int:
        """Get the embedding dimension"""
        return self.embedding_dim
