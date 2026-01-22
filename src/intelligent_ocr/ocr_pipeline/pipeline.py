"""Main OCR pipeline orchestrator."""

from pathlib import Path
from typing import Dict, Any, Optional

from intelligent_ocr.domain.enums import DocumentType
from intelligent_ocr.domain.schemas.ocr import OCRResult, TextBlock
from intelligent_ocr.domain.schemas.layout import LayoutDetectionResult
from intelligent_ocr.domain.schemas.extraction import ExtractionResult, ExtractedField
from intelligent_ocr.core.exceptions import OCRPipelineError


class OCRPipeline:
    """Main OCR pipeline for processing documents."""
    
    def __init__(self):
        """Initialize OCR pipeline."""
        from intelligent_ocr.ocr_pipeline.text_recognition import create_tesseract_engine
        self.ocr_engine = create_tesseract_engine()
    
    def process(
        self,
        file_path: Path,
        document_type: DocumentType = DocumentType.AUTO,
        language: str = "eng"
    ) -> Dict[str, Any]:
        """
        Process document through OCR pipeline.
        
        Args:
            file_path: Path to document file
            document_type: Type of document to process
            language: OCR language code
            
        Returns:
            Dictionary containing processing results
        """
        try:
            # Step 1: Preprocessing (placeholder)
            preprocessed_image = self._preprocess(file_path)
            
            # Step 2: Layout Detection
            layout_result = self._detect_layout(preprocessed_image, document_type)
            
            # Step 3: OCR Text Recognition
            ocr_result = self._recognize_text(preprocessed_image, layout_result, language)
            
            # Step 4: Semantic Extraction
            # Map OCR language code to spaCy language code (e.g., "eng" -> "en")
            spacy_lang = self._map_language_code(language)
            extraction_result = self._extract_semantics(
                ocr_result,
                layout_result,
                document_type,
                language=spacy_lang
            )
            
            return {
                "layout": layout_result.model_dump() if layout_result else None,
                "ocr": ocr_result.model_dump() if ocr_result else None,
                "extraction": extraction_result.model_dump() if extraction_result else None,
            }
        except Exception as e:
            raise OCRPipelineError(f"Pipeline processing failed: {str(e)}")
    
    def _preprocess(self, file_path: Path) -> Any:
        """
        Preprocess image/document.
        
        Loads image and applies preprocessing pipeline:
        - Grayscale conversion
        - Contrast enhancement
        - Deskewing
        - Noise removal
        - Binarization
        """
        import cv2
        from intelligent_ocr.ocr_pipeline.preprocessing import preprocess_from_file
        
        # Load and preprocess image
        result = preprocess_from_file(
            file_path,
            deskew=True,
            denoise=True,
            binarize=True,
            denoise_method="bilateral",
            binarize_method="otsu",
            enhance_contrast=True
        )
        
        return result["processed_image"]
    
    def _detect_layout(
        self,
        image: Any,
        document_type: DocumentType
    ) -> LayoutDetectionResult:
        """
        Detect document layout.
        
        Returns layout with page dimensions. Regions list may be empty
        if layout detection is not implemented yet.
        """
        import numpy as np
        
        # Get image dimensions
        if isinstance(image, np.ndarray):
            height, width = image.shape[:2]
        else:
            height, width = 0, 0
        
        return LayoutDetectionResult(
            regions=[],  # Layout detection to be implemented
            page_width=width,
            page_height=height
        )
    
    def _recognize_text(
        self,
        image: Any,
        layout_result: LayoutDetectionResult,
        language: str
    ) -> OCRResult:
        """
        Perform OCR text recognition using Tesseract.
        
        If layout regions are detected, extracts text from each region.
        Otherwise, extracts text from the entire image.
        
        Args:
            image: Preprocessed image
            layout_result: Layout detection result with regions
            language: OCR language code
            
        Returns:
            OCRResult with extracted text blocks
        """
        # If regions are detected, extract from each region
        if layout_result.regions:
            return self.ocr_engine.extract_from_regions(
                image=image,
                regions=layout_result.regions,
                language=language
            )
        else:
            # Extract from entire image
            return self.ocr_engine.extract_full_image(
                image=image,
                language=language
            )
    
    def _map_language_code(self, ocr_lang: str) -> str:
        """
        Map OCR language code to spaCy language code.
        
        Args:
            ocr_lang: OCR language code (e.g., "eng", "fra")
            
        Returns:
            spaCy language code (e.g., "en", "fr")
        """
        lang_map = {
            "eng": "en",
            "fra": "fr",
            "deu": "de",
            "spa": "es",
            "ara": "ar",
        }
        return lang_map.get(ocr_lang[:3].lower(), "en")
    
    def _extract_semantics(
        self,
        ocr_result: OCRResult,
        layout_result: LayoutDetectionResult,
        document_type: DocumentType,
        language: str = "en"
    ) -> ExtractionResult:
        """
        Extract semantic information from OCR results.
        
        Args:
            ocr_result: OCR result with extracted text
            layout_result: Layout detection result
            document_type: Type of document
            language: Language code for extraction
            
        Returns:
            ExtractionResult with extracted semantic fields
        """
        from intelligent_ocr.ocr_pipeline.semantic_extraction import (
            FormsExtractor,
            CVExtractor,
            InvoiceExtractor,
            BaseSemanticExtractor
        )
        
        # Select appropriate extractor based on document type
        if document_type == DocumentType.FORM:
            extractor = FormsExtractor(language=language)
        elif document_type == DocumentType.CV:
            extractor = CVExtractor(language=language)
        elif document_type == DocumentType.INVOICE:
            extractor = InvoiceExtractor(language=language)
        else:
            # Default to base extractor
            extractor = BaseSemanticExtractor(language=language)
            return extractor.extract_from_ocr_result(ocr_result)
        
        return extractor.extract(ocr_result, layout_result, document_type)
