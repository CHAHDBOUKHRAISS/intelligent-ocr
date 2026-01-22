"""Metadata endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from intelligent_ocr.domain.enums import DocumentType, OutputFormat

router = APIRouter(prefix="/metadata", tags=["metadata"])


class SupportedTypesResponse(BaseModel):
    """Response for supported document types."""
    document_types: List[str]
    output_formats: List[str]
    supported_languages: List[str]


@router.get("/supported-types", response_model=SupportedTypesResponse)
async def get_supported_types():
    """Get supported document types and formats."""
    return SupportedTypesResponse(
        document_types=[dt.value for dt in DocumentType],
        output_formats=[of.value for of in OutputFormat],
        supported_languages=["eng", "fra", "ara"]  # Example languages
    )
