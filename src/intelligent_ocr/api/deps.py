"""FastAPI dependencies."""

from intelligent_ocr.services.document_service import DocumentService
from intelligent_ocr.services.export_service import ExportService
from intelligent_ocr.services.storage_service import StorageService


def get_document_service() -> DocumentService:
    """Dependency for document service."""
    return DocumentService()


def get_export_service() -> ExportService:
    """Dependency for export service."""
    return ExportService()


def get_storage_service() -> StorageService:
    """Dependency for storage service."""
    return StorageService()
