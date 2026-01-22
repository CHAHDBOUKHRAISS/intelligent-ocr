"""Semantic extraction schemas."""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ExtractedField(BaseModel):
    """Extracted semantic field."""
    field_name: str = Field(description="Field name/key")
    value: Any = Field(description="Extracted value")
    confidence: float = Field(description="Extraction confidence", ge=0.0, le=1.0)
    source_region: Optional[str] = Field(default=None, description="Source layout region ID")


class ExtractionResult(BaseModel):
    """Semantic extraction result."""
    fields: Dict[str, ExtractedField] = Field(default_factory=dict, description="Extracted fields")
    raw_data: Dict[str, Any] = Field(default_factory=dict, description="Additional raw data")
