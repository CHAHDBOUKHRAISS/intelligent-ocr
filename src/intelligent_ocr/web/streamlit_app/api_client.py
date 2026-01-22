"""API client for communicating with FastAPI backend."""

import requests
from typing import Optional, Dict, Any
import io


class APIClient:
    """Client for interacting with Intelligent OCR API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL of the FastAPI backend
        """
        self.base_url = base_url.rstrip("/")
    
    def health_check(self) -> bool:
        """Check if API is available."""
        try:
            response = requests.get(f"{self.base_url}/health/", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def upload_and_process(
        self,
        file: io.BytesIO,
        filename: str,
        document_type: str = "auto",
        language: str = "eng",
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Upload and process document.
        
        Args:
            file: File-like object to upload
            filename: Name of the file
            document_type: Type of document (form, cv, invoice, auto)
            language: OCR language code
            output_format: Output format (json or csv)
            
        Returns:
            Response data from API
        """
        url = f"{self.base_url}/documents/upload-and-process"
        
        files = {"file": (filename, file, "application/octet-stream")}
        params = {
            "document_type": document_type,
            "language": language,
            "output_format": output_format
        }
        
        response = requests.post(url, files=files, params=params, timeout=300)
        response.raise_for_status()
        
        if output_format == "csv":
            return {"csv_data": response.text, "format": "csv"}
        else:
            return response.json()
    
    def get_supported_types(self) -> Dict[str, Any]:
        """Get supported document types and formats."""
        url = f"{self.base_url}/metadata/supported-types"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
