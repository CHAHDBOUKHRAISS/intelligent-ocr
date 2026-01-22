"""Layout detection schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """Bounding box coordinates."""
    x: int = Field(description="X coordinate (left)")
    y: int = Field(description="Y coordinate (top)")
    width: int = Field(description="Width")
    height: int = Field(description="Height")


class LayoutRegion(BaseModel):
    """Detected layout region."""
    region_id: str = Field(description="Unique region identifier")
    region_type: str = Field(description="Type of region (text, table, checkbox, etc.)")
    bounding_box: BoundingBox = Field(description="Bounding box coordinates")
    confidence: float = Field(description="Detection confidence score", ge=0.0, le=1.0)


class LayoutDetectionResult(BaseModel):
    """Result of layout detection."""
    regions: List[LayoutRegion] = Field(default_factory=list, description="Detected regions")
    page_width: int = Field(description="Page width in pixels")
    page_height: int = Field(description="Page height in pixels")
