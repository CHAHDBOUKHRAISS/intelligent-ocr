"""Base semantic extractor using spaCy for NER and rule-based patterns."""

import re
import spacy
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime

from intelligent_ocr.domain.schemas.extraction import ExtractedField, ExtractionResult
from intelligent_ocr.domain.schemas.ocr import OCRResult, TextBlock


class BaseSemanticExtractor:
    """Base semantic extractor using spaCy NER and rule-based patterns."""
    
    def __init__(self, language: str = "en"):
        """
        Initialize semantic extractor.
        
        Args:
            language: Language code for spaCy model (e.g., "en", "fr")
        """
        self.language = language
        try:
            model_name = "en_core_web_sm" if language == "en" else f"{language}_core_news_sm"
            self.nlp = spacy.load(model_name)
        except OSError:
            self.nlp = spacy.blank(language)
    
    def extract_names(self, text: str) -> List[Tuple[str, float]]:
        """
        Extract person names from text using NER.
        
        Args:
            text: Input text
            
        Returns:
            List of tuples (name, confidence)
        """
        names = []
        doc = self.nlp(text)
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                if len(ent.text.strip()) > 2:
                    names.append((ent.text.strip(), 0.85))
        
        return names
    
    def extract_dates(self, text: str) -> List[Tuple[str, float]]:
        """
        Extract dates from text using NER and regex patterns.
        
        Args:
            text: Input text
            
        Returns:
            List of tuples (date_string, confidence)
        """
        dates = []
        
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "DATE":
                dates.append((ent.text.strip(), 0.80))
        
        date_patterns = [
            # MM/DD/YYYY or DD/MM/YYYY
            (r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', 0.75),
            # YYYY-MM-DD
            (r'\b\d{4}-\d{2}-\d{2}\b', 0.85),
            # DD Month YYYY
            (r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b', 0.80),
            # Month DD, YYYY
            (r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b', 0.80),
        ]
        
        for pattern, confidence in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                date_str = match.group().strip()
                if not any(d[0] == date_str for d in dates):
                    dates.append((date_str, confidence))
        
        return dates
    
    def extract_emails(self, text: str) -> List[Tuple[str, float]]:
        """
        Extract email addresses using regex pattern.
        
        Args:
            text: Input text
            
        Returns:
            List of tuples (email, confidence)
        """
        emails = []
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        matches = re.finditer(email_pattern, text)
        for match in matches:
            email = match.group().strip()
            emails.append((email, 0.95))  
        
        return emails
    
    def extract_monetary_amounts(self, text: str) -> List[Tuple[str, float]]:
        """
        Extract monetary amounts using NER and regex patterns.
        
        Args:
            text: Input text
            
        Returns:
            List of tuples (amount_string, confidence)
        """
        amounts = []
        
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "MONEY":
                amounts.append((ent.text.strip(), 0.85))
        
        currency_symbols = r'[$€£¥₹]|USD|EUR|GBP|JPY|INR'
        
        pattern1 = rf'\b{currency_symbols}\s*\d+(?:,\d{{3}})*(?:\.\d{{2}})?\b'
        matches = re.finditer(pattern1, text, re.IGNORECASE)
        for match in matches:
            amount = match.group().strip()
            if not any(a[0] == amount for a in amounts):
                amounts.append((amount, 0.90))
        
        pattern2 = rf'\b\d+(?:,\d{{3}})*(?:\.\d{{2}})?\s*(?:{currency_symbols})\b'
        matches = re.finditer(pattern2, text, re.IGNORECASE)
        for match in matches:
            amount = match.group().strip()
            if not any(a[0] == amount for a in amounts):
                amounts.append((amount, 0.90))
        
        currency_words = r'dollars?|euros?|pounds?|rupees?|yen'
        pattern3 = rf'\b\d+(?:,\d{{3}})*(?:\.\d{{2}})?\s*(?:{currency_words})\b'
        matches = re.finditer(pattern3, text, re.IGNORECASE)
        for match in matches:
            amount = match.group().strip()
            if not any(a[0] == amount for a in amounts):
                amounts.append((amount, 0.85))
        
        return amounts
    
    def extract_all(self, text: str) -> Dict[str, List[Tuple[str, float]]]:
        """
        Extract all semantic information from text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with extracted entities by type
        """
        return {
            "names": self.extract_names(text),
            "dates": self.extract_dates(text),
            "emails": self.extract_emails(text),
            "monetary_amounts": self.extract_monetary_amounts(text)
        }
    
    def extract_from_ocr_result(
        self,
        ocr_result: OCRResult,
        region_id: Optional[str] = None
    ) -> ExtractionResult:
        """
        Extract semantic information from OCR result.
        
        Args:
            ocr_result: OCR result containing extracted text
            region_id: Optional region ID for tracking source
            
        Returns:
            ExtractionResult with extracted fields
        """
        fields = {}
        
        full_text = ocr_result.full_text
        if full_text:
            extracted = self.extract_all(full_text)
            
            if extracted["names"]:
                names = [name for name, _ in extracted["names"]]
                fields["names"] = ExtractedField(
                    field_name="names",
                    value=names[0] if len(names) == 1 else names,
                    confidence=max([conf for _, conf in extracted["names"]]),
                    source_region=region_id
                )
            
            if extracted["dates"]:
                dates = [date for date, _ in extracted["dates"]]
                fields["dates"] = ExtractedField(
                    field_name="dates",
                    value=dates[0] if len(dates) == 1 else dates,
                    confidence=max([conf for _, conf in extracted["dates"]]),
                    source_region=region_id
                )
            
            if extracted["emails"]:
                emails = [email for email, _ in extracted["emails"]]
                fields["emails"] = ExtractedField(
                    field_name="emails",
                    value=emails[0] if len(emails) == 1 else emails,
                    confidence=max([conf for _, conf in extracted["emails"]]),
                    source_region=region_id
                )
            
            if extracted["monetary_amounts"]:
                amounts = [amount for amount, _ in extracted["monetary_amounts"]]
                fields["monetary_amounts"] = ExtractedField(
                    field_name="monetary_amounts",
                    value=amounts[0] if len(amounts) == 1 else amounts,
                    confidence=max([conf for _, conf in extracted["monetary_amounts"]]),
                    source_region=region_id
                )
        
        for block in ocr_result.blocks:
            if block.text and block.text.strip():
                block_extracted = self.extract_all(block.text)
                
                for entity_type, entities in block_extracted.items():
                    if entities:
                        field_name = entity_type
                        if field_name not in fields:
                            values = [val for val, _ in entities]
                            fields[field_name] = ExtractedField(
                                field_name=field_name,
                                value=values[0] if len(values) == 1 else values,
                                confidence=max([conf for _, conf in entities]),
                                source_region=block.region_id or region_id
                            )
                        else:
                            existing_conf = fields[field_name].confidence
                            new_conf = max([conf for _, conf in entities])
                            if new_conf > existing_conf:
                                values = [val for val, _ in entities]
                                fields[field_name] = ExtractedField(
                                    field_name=field_name,
                                    value=values[0] if len(values) == 1 else values,
                                    confidence=new_conf,
                                    source_region=block.region_id or region_id
                                )
        
        return ExtractionResult(
            fields=fields,
            raw_data={
                "extraction_method": "spacy_ner_and_regex",
                "language": self.language
            }
        )
