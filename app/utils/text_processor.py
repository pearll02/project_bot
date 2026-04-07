"""Text processing utilities"""
import tiktoken
from typing import List
from app.utils.logger import logger


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens in text using tiktoken"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception as e:
        logger.warning(f"Error counting tokens: {str(e)}, using estimate")
        # Fallback: approximate 1 token = 4 characters
        return len(text) // 4


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
    model: str = "gpt-4"
) -> List[str]:
    """
    Split text into overlapping chunks based on token count
    
    Args:
        text: Text to chunk
        chunk_size: Target size in tokens
        chunk_overlap: Overlap size in tokens
        model: Model name for token counting
    
    Returns:
        List of text chunks
    """
    # For simplicity, split by sentences/paragraphs and approximate tokens
    encoding = tiktoken.encoding_for_model(model)
    
    # Split by paragraphs first
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # Check if adding this paragraph would exceed chunk size
        test_text = current_chunk + "\n\n" + paragraph if current_chunk else paragraph
        token_count = len(encoding.encode(test_text))
        
        if token_count > chunk_size and current_chunk:
            # Save current chunk and start new one
            chunks.append(current_chunk)
            current_chunk = paragraph
        else:
            current_chunk = test_text
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(current_chunk)
    
    # Add overlap between chunks
    if chunk_overlap > 0:
        overlapped_chunks = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                overlapped_chunks.append(chunk)
            else:
                # Find overlap from previous chunk
                prev_chunk = chunks[i - 1]
                # Take last overlap_size tokens from previous chunk
                prev_tokens = encoding.encode(prev_chunk)
                overlap_tokens = prev_tokens[-min(chunk_overlap, len(prev_tokens)):]
                overlap_text = encoding.decode(overlap_tokens)
                
                combined = overlap_text + "\n" + chunk
                overlapped_chunks.append(combined)
        
        chunks = overlapped_chunks
    
    logger.info(f"Text chunked into {len(chunks)} chunks")
    return chunks


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove control characters
    text = ''.join(c for c in text if c.isprintable() or c in '\n\t')
    return text.strip()
