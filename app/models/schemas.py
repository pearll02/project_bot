"""Request/Response schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DocumentMetadata(BaseModel):
    """Metadata for a stored document"""
    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="File type: pdf or txt")
    chunks_count: int = Field(..., description="Number of text chunks")
    created_at: datetime = Field(..., description="Upload timestamp")
    

class UploadResponse(BaseModel):
    """Response for document upload"""
    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Uploaded filename")
    file_type: str = Field(..., description="File type: pdf or txt")
    chunks_count: int = Field(..., description="Number of chunks created")
    message: str = Field(..., description="Success message")


class QueryRequest(BaseModel):
    """Request for asking a question"""
    question: str = Field(..., min_length=1, max_length=2000, description="Question to ask")
    document_id: str = Field(..., description="Document ID to search in")
    top_k: Optional[int] = Field(5, ge=1, le=20, description="Number of chunks to retrieve")
    include_context: Optional[bool] = Field(True, description="Include source context in response")


class QueryResponse(BaseModel):
    """Response for a question"""
    answer: str = Field(..., description="Generated answer")
    document_id: str = Field(..., description="Document ID searched")
    chunks_used: int = Field(..., description="Number of chunks used")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    sources: Optional[List[str]] = Field(None, description="Source chunks used")


class ChatMessage(BaseModel):
    """A message in chat history"""
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatSession(BaseModel):
    """Chat session history"""
    session_id: str = Field(..., description="Unique session identifier")
    document_id: str = Field(..., description="Associated document ID")
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Error response"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    status_code: int = Field(..., description="HTTP status code")
