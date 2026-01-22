"""Storage service for file management."""

import shutil
from pathlib import Path
from typing import BinaryIO, Optional
import uuid

from intelligent_ocr.config.settings import settings
from intelligent_ocr.core.exceptions import StorageError
from intelligent_ocr.core.utils import generate_document_id


class StorageService:
    """Service for managing file storage."""
    
    def __init__(self):
        self.upload_dir = settings.upload_dir
        self.storage_dir = settings.storage_dir
    
    def save_uploaded_file(
        self,
        file: BinaryIO,
        filename: str,
        document_id: Optional[str] = None
    ) -> Path:
        """
        Save uploaded file to storage.
        
        Args:
            file: File-like object to save
            filename: Original filename
            document_id: Optional document ID (generated if not provided)
            
        Returns:
            Path to saved file
        """
        if document_id is None:
            document_id = generate_document_id()
        
        # Create document-specific directory
        doc_dir = self.upload_dir / document_id
        doc_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = doc_dir / filename
        
        try:
            file.seek(0)  # Reset file pointer
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file, f)
            
            return file_path
        except Exception as e:
            raise StorageError(f"Failed to save file: {str(e)}")
    
    def get_file_path(self, document_id: str, filename: str) -> Path:
        """Get path to stored file."""
        return self.upload_dir / document_id / filename
    
    def file_exists(self, document_id: str, filename: str) -> bool:
        """Check if file exists."""
        return self.get_file_path(document_id, filename).exists()
    
    def cleanup(self, document_id: str) -> None:
        """Clean up files for a document."""
        doc_dir = self.upload_dir / document_id
        if doc_dir.exists():
            shutil.rmtree(doc_dir)
