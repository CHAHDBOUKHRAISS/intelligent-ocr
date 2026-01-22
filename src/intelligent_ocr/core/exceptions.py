"""Custom exceptions for the OCR system."""


class OCRException(Exception):
    """Base exception for OCR-related errors."""
    pass


class OCRPipelineError(OCRException):
    """Raised when OCR pipeline processing fails."""
    pass


class InvalidDocumentTypeError(OCRPipelineError):
    """Raised when document type is invalid or unsupported."""
    pass


class FileValidationError(OCRException):
    """Raised when file validation fails."""
    pass


class StorageError(OCRException):
    """Raised when storage operations fail."""
    pass
