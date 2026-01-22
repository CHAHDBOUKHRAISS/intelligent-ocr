"""Domain enumerations for document types and processing options."""

from enum import Enum


class DocumentType(str, Enum):
    """Supported document types."""
    FORM = "form"
    CV = "cv"
    INVOICE = "invoice"
    AUTO = "auto"  # Auto-detect document type


class OutputFormat(str, Enum):
    """Supported output formats."""
    JSON = "json"
    CSV = "csv"


class ProcessingStatus(str, Enum):
    """OCR processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
