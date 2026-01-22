"""Invoice-specific semantic extractor."""

from intelligent_ocr.domain.enums import DocumentType
from intelligent_ocr.domain.schemas.ocr import OCRResult
from intelligent_ocr.domain.schemas.layout import LayoutDetectionResult
from intelligent_ocr.domain.schemas.extraction import ExtractionResult
from intelligent_ocr.ocr_pipeline.semantic_extraction.base_extractor import BaseSemanticExtractor


class InvoiceExtractor:
    """Extractor for invoice documents."""
    
    def __init__(self, language: str = "en"):
        """
        Initialize invoice extractor.
        
        Args:
            language: Language code for extraction
        """
        self.base_extractor = BaseSemanticExtractor(language=language)
    
    def extract(
        self,
        ocr_result: OCRResult,
        layout_result: LayoutDetectionResult,
        document_type: DocumentType = DocumentType.INVOICE
    ) -> ExtractionResult:
        """
        Extract semantic information from invoice document.
        
        Args:
            ocr_result: OCR result with extracted text
            layout_result: Layout detection result
            document_type: Type of document
            
        Returns:
            ExtractionResult with extracted fields
        """
        result = self.base_extractor.extract_from_ocr_result(ocr_result)
        
        return result
