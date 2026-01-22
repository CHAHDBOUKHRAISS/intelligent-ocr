"""Text recognition module for OCR."""

from intelligent_ocr.ocr_pipeline.text_recognition.engine_tesseract import (
    TesseractEngine,
    create_tesseract_engine
)

__all__ = ["TesseractEngine", "create_tesseract_engine"]
