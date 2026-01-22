"""Application configuration settings."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "Intelligent OCR API"
    api_version: str = "1.0.0"
    
    # File Upload Settings
    max_file_size_mb: int = 50
    allowed_extensions: str = ".jpg,.jpeg,.png,.tiff,.tif,.bmp,.webp,.pdf"
    upload_dir: Path = Path("data/raw")
    
    # Output Settings
    output_json_dir: Path = Path("outputs/json")
    output_csv_dir: Path = Path("outputs/csv")
    
    # OCR Settings
    default_language: str = "eng"
    ocr_engine: str = "tesseract"  # Options: tesseract, ml_model
    
    # Storage Settings
    storage_dir: Path = Path("data/processed")
    keep_processed_files: bool = True
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Ensure directories exist
settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.output_json_dir.mkdir(parents=True, exist_ok=True)
settings.output_csv_dir.mkdir(parents=True, exist_ok=True)
settings.storage_dir.mkdir(parents=True, exist_ok=True)
