"""Document upload router"""
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import Optional
from app.models.schemas import UploadResponse
from app.config import settings
from app.services import get_document_service
from app.utils.file_handler import (
    validate_file_extension,
    get_file_size,
    save_uploaded_file
)
from app.utils.logger import logger

router = APIRouter(prefix="/api", tags=["documents"])


@router.post("/upload", response_model=UploadResponse, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
) -> UploadResponse:
    """
    Upload and process a document
    
    **Supported formats:** PDF, TXT
    **Max file size:** 50MB
    
    Returns document ID for use in queries
    """
    try:
        # Validate file
        if not validate_file_extension(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: PDF, TXT"
            )
        
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {settings.max_file_size / 1024 / 1024}MB"
            )
        
        logger.info(f"Uploading file: {file.filename}")
        
        # Save file
        file_path = save_uploaded_file(
            content,
            file.filename,
            settings.upload_dir_path
        )
        
        # Get document service and process document
        document_service = get_document_service()
        result = document_service.process_document(file_path, file.filename)
        
        return UploadResponse(
            document_id=result['document_id'],
            filename=result['filename'],
            file_type=result['file_type'],
            chunks_count=result['chunks_count'],
            message=f"Document uploaded successfully. Created {result['chunks_count']} chunks."
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading document: {str(e)}"
        )


@router.get("/documents/{document_id}")
async def get_document_info(document_id: str):
    """Get information about a stored document"""
    try:
        document_service = get_document_service()
        info = document_service.get_document_info(document_id)
        
        if not info:
            raise HTTPException(
                status_code=404,
                detail=f"Document {document_id} not found"
            )
        
        return info
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document"""
    try:
        document_service = get_document_service()
        success = document_service.delete_document(document_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Document {document_id} not found"
            )
        
        return {"message": f"Document {document_id} deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
