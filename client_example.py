"""Example and testing module for API requests"""
# This file demonstrates how to use the API with Python requests

import requests
import json
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = None  # Not used in current implementation, but can be added


class DocumentQAChatbot:
    """Client for Document QA Chatbot API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    def upload_document(self, file_path: str) -> dict:
        """Upload a document for Q&A"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(
                f"{self.base_url}/api/upload",
                files=files
            )
            return response.json()
    
    def ask_question(
        self,
        question: str,
        document_id: str,
        top_k: int = 5,
        include_context: bool = True
    ) -> dict:
        """Ask a question about a document"""
        payload = {
            "question": question,
            "document_id": document_id,
            "top_k": top_k,
            "include_context": include_context
        }
        response = self.session.post(
            f"{self.base_url}/api/query",
            json=payload
        )
        return response.json()
    
    def get_document_info(self, document_id: str) -> dict:
        """Get information about a document"""
        response = self.session.get(
            f"{self.base_url}/api/documents/{document_id}"
        )
        return response.json()
    
    def delete_document(self, document_id: str) -> dict:
        """Delete a document"""
        response = self.session.delete(
            f"{self.base_url}/api/documents/{document_id}"
        )
        return response.json()
    
    def health_check(self) -> dict:
        """Check API health"""
        response = self.session.get(f"{self.base_url}/health")
        return response.json()


if __name__ == "__main__":
    # Example usage
    client = DocumentQAChatbot()
    
    # Check health
    print("Health Check:")
    print(json.dumps(client.health_check(), indent=2))
