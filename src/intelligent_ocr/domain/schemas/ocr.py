"""OCR-related schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class TextBlock(BaseModel):
    """OCR text block."""
    text: str = Field(description="Extracted text")
    confidence: float = Field(description="OCR confidence score", ge=0.0, le=1.0)
    bounding_box: Optional["BoundingBox"] = Field(default=None, description="Text bounding box")
    region_id: Optional[str] = Field(default=None, description="Associated layout region ID")


class OCRResult(BaseModel):
    """OCR processing result."""
    blocks: List[TextBlock] = Field(default_factory=list, description="Extracted text blocks")
    full_text: str = Field(default="", description="Full extracted text")
    average_confidence: float = Field(description="Average confidence score", ge=0.0, le=1.0)
