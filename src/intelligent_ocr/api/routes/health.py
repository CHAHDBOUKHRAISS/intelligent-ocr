"""Health check endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    from intelligent_ocr.config.settings import settings
    
    return HealthResponse(
        status="healthy",
        version=settings.api_version
    )


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    return {"status": "ready"}
