"""RAG (Retrieval-Augmented Generation) service"""
from typing import List, Tuple
import google.generativeai as genai
from app.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.utils.logger import logger


class RAGService:
    """Service for RAG-based question answering using Google Gemini"""
    
    def __init__(self, vector_store: VectorStore):
        genai.configure(api_key=settings.gemini_api_key)
        self.embedding_service = EmbeddingService()
        self.vector_store = vector_store
        self.model = genai.GenerativeModel(settings.gemini_model)
    
    def answer_question(
        self,
        question: str,
        document_id: str,
        top_k: int = None,
        include_context: bool = True
    ) -> Tuple[str, int, float, List[str]]:
        """
        Answer a question based on document context
        
        Args:
            question: User's question
            document_id: Document to search in
            top_k: Number of chunks to retrieve
            include_context: Include source chunks in response
        
        Returns:
            Tuple of (answer, chunks_used, confidence_score, source_chunks)
        """
        if top_k is None:
            top_k = settings.top_k_chunks
        
        try:
            # Step 1: Embed the question
            logger.info(f"Processing question: {question}")
            question_embedding = self.embedding_service.generate_single_embedding(question)
            
            # Step 2: Search for relevant chunks
            relevant_chunks = self.vector_store.search(
                question_embedding,
                top_k=top_k,
                document_id=document_id
            )
            
            if not relevant_chunks:
                return "Answer not found in document.", 0, 0.0, []
            
            # Step 3: Build context from relevant chunks
            context_text = "\n---\n".join([chunk[0] for chunk in relevant_chunks])
            confidence = sum(score for _, score in relevant_chunks) / len(relevant_chunks)
            
            # Step 4: Generate answer using LLM (Gemini)
            answer = self._generate_answer(question, context_text)
            
            logger.info(f"Generated answer with {len(relevant_chunks)} chunks")
            
            return (
                answer,
                len(relevant_chunks),
                confidence,
                [chunk[0] for chunk in relevant_chunks] if include_context else []
            )
        
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise
    
    def _generate_answer(self, question: str, context: str) -> str:
        """
        Generate answer using Gemini with context
        
        Args:
            question: User's question
            context: Relevant document chunks
        
        Returns:
            Generated answer
        """
        system_prompt = """You are a helpful assistant that answers questions based on provided document context.
IMPORTANT RULES:
1. Answer ONLY from the provided context
2. If the answer cannot be found in the context, respond with "The answer cannot be found in the provided document."
3. Be concise and accurate
4. Provide specific quotes or references when helpful
5. Never make up information or use knowledge outside the provided context"""
        
        user_prompt = f"""{system_prompt}

Context from document:
{context}

Question: {question}

Please provide an accurate answer based only on the context above."""
        
        try:
            response = self.model.generate_content(user_prompt)
            return response.text
        
        except Exception as e:
            logger.error(f"Error generating answer with Gemini: {str(e)}")
            raise
