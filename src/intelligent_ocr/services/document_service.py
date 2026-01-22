"""Document processing service."""

from pathlib import Path
from typing import Dict, Any
import mimetypes

from intelligent_ocr.domain.enums import DocumentType, ProcessingStatus
from intelligent_ocr.domain.schemas.document import DocumentMetadata
from intelligent_ocr.core.utils import (
    generate_document_id,
    is_supported_file,
    get_file_extension
)
from intelligent_ocr.core.exceptions import FileValidationError, InvalidDocumentTypeError
from intelligent_ocr.ocr_pipeline.pipeline import OCRPipeline
from intelligent_ocr.services.storage_service import StorageService


class DocumentService:
    """Service for document processing."""
    
    def __init__(self):
        self.ocr_pipeline = OCRPipeline()
        self.storage_service = StorageService()
    
    def validate_file(self, filename: str, file_size: int) -> None:
        """
        Validate uploaded file.
        
        Args:
            filename: Name of the file
            file_size: Size of file in bytes
            
        Raises:
            FileValidationError: If file is invalid
        """
        if not filename:
            raise FileValidationError("Filename is required")
        
        if not is_supported_file(filename):
            raise FileValidationError(
                f"Unsupported file type. Supported: images (jpg, png, etc.) and PDF"
            )
        
        max_size = 50 * 1024 * 1024  # 50 MB
        if file_size > max_size:
            raise FileValidationError(f"File size exceeds maximum of {max_size / 1024 / 1024} MB")
    
    def detect_document_type(self, filename: str, auto_detect: bool = True) -> DocumentType:
        """
        Detect document type from filename or content.
        
        Args:
            filename: Name of the file
            auto_detect: Whether to auto-detect type
            
        Returns:
            Detected document type
        """
        if not auto_detect:
            return DocumentType.FORM
        
        # Simple heuristic: check filename for keywords
        filename_lower = filename.lower()
        if "cv" in filename_lower or "resume" in filename_lower:
            return DocumentType.CV
        elif "invoice" in filename_lower or "bill" in filename_lower:
            return DocumentType.INVOICE
        else:
            return DocumentType.FORM
    
    def process_document(
        self,
        file_path: Path,
        document_type: DocumentType,
        language: str = "eng"
    ) -> Dict[str, Any]:
        """
        Process document through OCR pipeline.
        
        Args:
            file_path: Path to document file
            document_type: Type of document
            language: OCR language code
            
        Returns:
            Processing results dictionary
        """
        if document_type == DocumentType.AUTO:
            document_type = self.detect_document_type(file_path.name)
        
        results = self.ocr_pipeline.process(
            file_path=file_path,
            document_type=document_type,
            language=language
        )
        
        return {
            "document_type": document_type.value,
            "language": language,
            **results
        }
    
    def create_metadata(
        self,
        document_id: str,
        filename: str,
        file_size: int,
        document_type: DocumentType,
        status: ProcessingStatus = ProcessingStatus.PENDING
    ) -> DocumentMetadata:
        """Create document metadata."""
        from datetime import datetime
        
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = "application/octet-stream"
        
        return DocumentMetadata(
            document_id=document_id,
            filename=filename,
            document_type=document_type,
            upload_timestamp=datetime.now(),
            status=status,
            file_size=file_size,
            mime_type=mime_type
        )
