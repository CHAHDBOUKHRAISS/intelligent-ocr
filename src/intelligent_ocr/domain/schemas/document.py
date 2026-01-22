"""Document-related schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from intelligent_ocr.domain.enums import DocumentType, ProcessingStatus


class DocumentUpload(BaseModel):
    """Schema for document upload request."""
    document_type: DocumentType = Field(default=DocumentType.AUTO, description="Type of document")
    language: Optional[str] = Field(default="eng", description="OCR language code")


class DocumentMetadata(BaseModel):
    """Schema for document metadata."""
    document_id: str = Field(description="Unique document identifier")
    filename: str = Field(description="Original filename")
    document_type: DocumentType = Field(description="Detected or specified document type")
    upload_timestamp: datetime = Field(description="Upload timestamp")
    status: ProcessingStatus = Field(description="Processing status")
    file_size: int = Field(description="File size in bytes")
    mime_type: str = Field(description="MIME type of the file")
