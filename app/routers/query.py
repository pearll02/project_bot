"""Query/RAG router"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.config import settings
from app.services import get_vector_store, get_rag_service
from app.utils.logger import logger

router = APIRouter(prefix="/api", tags=["query"])


@router.post("/query", response_model=QueryResponse)
async def ask_question(request: QueryRequest) -> QueryResponse:
    """
    Ask a question about a document
    
    **Process:**
    1. Embeds the question
    2. Finds most relevant chunks using semantic search
    3. Passes context to LLM
    4. Returns generated answer
    """
    try:
        # Get services
        vector_store = get_vector_store()
        rag_service = get_rag_service()
        
        # Validate document exists
        chunks = vector_store.get_documents(request.document_id)
        if not chunks:
            raise HTTPException(
                status_code=404,
                detail=f"Document {request.document_id} not found"
            )
        
        logger.info(f"Processing query: {request.question[:50]}...")
        
        # Get answer using RAG
        answer, chunks_used, confidence, sources = rag_service.answer_question(
            question=request.question,
            document_id=request.document_id,
            top_k=request.top_k,
            include_context=request.include_context
        )
        
        return QueryResponse(
            answer=answer,
            document_id=request.document_id,
            chunks_used=chunks_used,
            confidence=confidence,
            sources=sources if request.include_context else None
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )
