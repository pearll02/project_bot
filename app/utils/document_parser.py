"""PDF and document parsing utilities"""
import pdfplumber
from pathlib import Path
from typing import Optional
from app.utils.logger import logger


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num} ---\n{page_text}"
        
        logger.info(f"Extracted text from PDF: {file_path}")
        return text
    except Exception as e:
        logger.error(f"Error extracting PDF text: {str(e)}")
        raise


def extract_text_from_txt(file_path: str, encoding: str = 'utf-8') -> str:
    """Extract text from text file"""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            text = f.read()
        
        logger.info(f"Extracted text from TXT: {file_path}")
        return text
    except UnicodeDecodeError:
        # Try with different encoding
        logger.warning(f"UTF-8 failed, trying latin-1 for {file_path}")
        with open(file_path, 'r', encoding='latin-1') as f:
            text = f.read()
        return text
    except Exception as e:
        logger.error(f"Error extracting TXT text: {str(e)}")
        raise


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        from docx import Document
        doc = Document(file_path)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        logger.info(f"Extracted text from DOCX: {file_path}")
        return text
    except ImportError:
        logger.warning("python-docx not installed, install to support DOCX files")
        raise ImportError("python-docx required for DOCX support")
    except Exception as e:
        logger.error(f"Error extracting DOCX text: {str(e)}")
        raise


def extract_text_from_file(file_path: str, file_type: str) -> str:
    """Generic function to extract text from any supported file"""
    if file_type == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_type == 'txt':
        return extract_text_from_txt(file_path)
    elif file_type == 'docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
