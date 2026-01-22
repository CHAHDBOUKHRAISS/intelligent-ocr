"""CV/Resume-specific semantic extractor."""

from intelligent_ocr.domain.enums import DocumentType
from intelligent_ocr.domain.schemas.ocr import OCRResult
from intelligent_ocr.domain.schemas.layout import LayoutDetectionResult
from intelligent_ocr.domain.schemas.extraction import ExtractionResult
from intelligent_ocr.ocr_pipeline.semantic_extraction.base_extractor import BaseSemanticExtractor


class CVExtractor:
    """Extractor for CV/Resume documents."""
    
    def __init__(self, language: str = "en"):
        """
        Initialize CV extractor.
        
        Args:
            language: Language code for extraction
        """
        self.base_extractor = BaseSemanticExtractor(language=language)
    
    def extract(
        self,
        ocr_result: OCRResult,
        layout_result: LayoutDetectionResult,
        document_type: DocumentType = DocumentType.CV
    ) -> ExtractionResult:
        """
        Extract semantic information from CV document.
        
        Args:
            ocr_result: OCR result with extracted text
            layout_result: Layout detection result
            document_type: Type of document
            
        Returns:
            ExtractionResult with extracted fields
        """
        # Use base extractor for general semantic extraction
        result = self.base_extractor.extract_from_ocr_result(ocr_result)
        
        # CV-specific enhancements can be added here
        # For example, extracting skills, work experience, education
        
        return result
