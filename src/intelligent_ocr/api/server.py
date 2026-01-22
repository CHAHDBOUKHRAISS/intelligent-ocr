"""FastAPI application server."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from intelligent_ocr.config.settings import settings
from intelligent_ocr.api.routes import health, documents, metadata


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="Intelligent OCR API for processing semi-structured documents"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(documents.router)
    app.include_router(metadata.router)
    
    return app


# Create app instance
app = create_app()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Intelligent OCR API",
        "version": settings.api_version,
        "docs": "/docs"
    }
