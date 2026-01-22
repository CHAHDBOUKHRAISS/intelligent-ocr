"""Tesseract OCR engine implementation."""

import pytesseract
import cv2
import numpy as np
from typing import List, Optional, Dict, Any
from pathlib import Path

from intelligent_ocr.domain.schemas.ocr import OCRResult, TextBlock
from intelligent_ocr.domain.schemas.layout import LayoutRegion, BoundingBox
from intelligent_ocr.core.exceptions import OCRPipelineError


class TesseractEngine:
    """Tesseract OCR engine for text extraction."""
    
    def __init__(self, tesseract_cmd: Optional[str] = None):
        """
        Initialize Tesseract engine.
        
        Args:
            tesseract_cmd: Path to tesseract executable (if not in PATH)
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    
    def extract_text(
        self,
        image: np.ndarray,
        language: str = "eng",
        config: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract text from entire image.
        
        Args:
            image: Preprocessed image (grayscale or binary)
            language: Tesseract language code (e.g., "eng", "fra", "ara")
            config: Tesseract config string (e.g., "--psm 6")
            
        Returns:
            Dictionary with text and confidence information
        """
        try:
            # Default config for single uniform block of text
            if config is None:
                config = "--psm 6"
            
            # Extract text with confidence scores
            data = pytesseract.image_to_data(
                image,
                lang=language,
                config=config,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text string
            text = pytesseract.image_to_string(image, lang=language, config=config).strip()
            
            # Calculate average confidence (excluding empty detections)
            confidences = [int(conf) for conf in data["conf"] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) / 100.0 if confidences else 0.0
            
            return {
                "text": text,
                "data": data,
                "average_confidence": avg_confidence
            }
        except Exception as e:
            raise OCRPipelineError(f"Tesseract OCR failed: {str(e)}")
    
    def extract_from_region(
        self,
        image: np.ndarray,
        bounding_box: BoundingBox,
        region_id: Optional[str] = None,
        language: str = "eng",
        config: Optional[str] = None
    ) -> TextBlock:
        """
        Extract text from a specific region of the image.
        
        Args:
            image: Full preprocessed image
            bounding_box: Bounding box coordinates for the region
            region_id: Optional region identifier
            language: Tesseract language code
            config: Tesseract config string
            
        Returns:
            TextBlock with extracted text and metadata
        """
        # Crop region from image
        x = bounding_box.x
        y = bounding_box.y
        w = bounding_box.width
        h = bounding_box.height
        
        # Ensure coordinates are within image bounds
        img_height, img_width = image.shape[:2]
        x = max(0, min(x, img_width))
        y = max(0, min(y, img_height))
        w = min(w, img_width - x)
        h = min(h, img_height - y)
        
        if w <= 0 or h <= 0:
            return TextBlock(
                text="",
                confidence=0.0,
                bounding_box=bounding_box,
                region_id=region_id
            )
        
        # Crop the region
        region_image = image[y:y+h, x:x+w]
        
        # Extract text from region
        try:
            result = self.extract_text(region_image, language=language, config=config)
            
            return TextBlock(
                text=result["text"],
                confidence=result["average_confidence"],
                bounding_box=bounding_box,
                region_id=region_id
            )
        except Exception as e:
            # Return empty block on error
            return TextBlock(
                text="",
                confidence=0.0,
                bounding_box=bounding_box,
                region_id=region_id
            )
    
    def extract_from_regions(
        self,
        image: np.ndarray,
        regions: List[LayoutRegion],
        language: str = "eng",
        config: Optional[str] = None
    ) -> OCRResult:
        """
        Extract text from multiple layout regions.
        
        Args:
            image: Preprocessed image
            regions: List of layout regions to extract text from
            language: Tesseract language code
            config: Tesseract config string (can be None for auto-detection)
            
        Returns:
            OCRResult with text blocks from all regions
        """
        text_blocks = []
        
        for region in regions:
            # Auto-select config based on region type
            region_config = self._get_config_for_region_type(region.region_type, config)
            
            # Extract text from region
            text_block = self.extract_from_region(
                image=image,
                bounding_box=region.bounding_box,
                region_id=region.region_id,
                language=language,
                config=region_config
            )
            
            text_blocks.append(text_block)
        
        # Combine all text
        full_text = "\n".join([block.text for block in text_blocks if block.text.strip()])
        
        # Calculate average confidence
        confidences = [block.confidence for block in text_blocks if block.confidence > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return OCRResult(
            blocks=text_blocks,
            full_text=full_text,
            average_confidence=avg_confidence
        )
    
    def extract_full_image(
        self,
        image: np.ndarray,
        language: str = "eng",
        config: Optional[str] = None
    ) -> OCRResult:
        """
        Extract text from entire image without region cropping.
        
        Args:
            image: Preprocessed image
            language: Tesseract language code
            config: Tesseract config string
            
        Returns:
            OCRResult with extracted text
        """
        if config is None:
            config = "--psm 6"  # Assume uniform block of text
        
        result = self.extract_text(image, language=language, config=config)
        
        # Create a single text block for the entire image
        img_height, img_width = image.shape[:2]
        bounding_box = BoundingBox(
            x=0,
            y=0,
            width=img_width,
            height=img_height
        )
        
        text_block = TextBlock(
            text=result["text"],
            confidence=result["average_confidence"],
            bounding_box=bounding_box,
            region_id=None
        )
        
        return OCRResult(
            blocks=[text_block],
            full_text=result["text"],
            average_confidence=result["average_confidence"]
        )
    
    def _get_config_for_region_type(
        self,
        region_type: str,
        default_config: Optional[str] = None
    ) -> str:
        """
        Get Tesseract config based on region type.
        
        PSM modes:
        - 6: Uniform block of text
        - 7: Single text line
        - 8: Single word
        - 11: Sparse text
        - 12: Single text line with OSD
        
        Args:
            region_type: Type of layout region
            default_config: Default config if provided
            
        Returns:
            Tesseract config string
        """
        if default_config:
            return default_config
        
        region_type_lower = region_type.lower()
        
        if "line" in region_type_lower or "textline" in region_type_lower:
            return "--psm 7"  # Single text line
        elif "word" in region_type_lower:
            return "--psm 8"  # Single word
        elif "table" in region_type_lower:
            return "--psm 6"  # Uniform block
        elif "sparse" in region_type_lower:
            return "--psm 11"  # Sparse text
        else:
            return "--psm 6"  # Default: uniform block


def create_tesseract_engine(tesseract_cmd: Optional[str] = None) -> TesseractEngine:
    """
    Factory function to create Tesseract engine instance.
    
    Args:
        tesseract_cmd: Path to tesseract executable
        
    Returns:
        TesseractEngine instance
    """
    return TesseractEngine(tesseract_cmd=tesseract_cmd)
