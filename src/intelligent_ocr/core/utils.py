"""Core utility functions."""

import uuid
from pathlib import Path
from typing import Optional


def generate_document_id() -> str:
    """Generate a unique document identifier."""
    return str(uuid.uuid4())


def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    return Path(filename).suffix.lower()


def is_image_file(filename: str) -> bool:
    """Check if file is an image."""
    image_extensions = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".webp"}
    return get_file_extension(filename) in image_extensions


def is_pdf_file(filename: str) -> bool:
    """Check if file is a PDF."""
    return get_file_extension(filename) == ".pdf"


def is_supported_file(filename: str) -> bool:
    """Check if file type is supported."""
    return is_image_file(filename) or is_pdf_file(filename)
