"""Export service for generating JSON and CSV outputs."""

import json
import csv
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from intelligent_ocr.config.settings import settings
from intelligent_ocr.domain.enums import OutputFormat
from intelligent_ocr.domain.schemas.extraction import ExtractionResult


class ExportService:
    """Service for exporting OCR results."""
    
    def __init__(self):
        self.json_dir = settings.output_json_dir
        self.csv_dir = settings.output_csv_dir
    
    def export_json(
        self,
        document_id: str,
        results: Dict[str, Any]
    ) -> Path:
        """
        Export results to JSON file.
        
        Args:
            document_id: Document identifier
            results: Results dictionary to export
            
        Returns:
            Path to exported JSON file
        """
        filename = f"{document_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path = self.json_dir / filename
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        return file_path
    
    def export_csv(
        self,
        document_id: str,
        extraction_result: ExtractionResult
    ) -> Path:
        """
        Export extraction results to CSV file.
        
        Args:
            document_id: Document identifier
            extraction_result: Extraction result to export
            
        Returns:
            Path to exported CSV file
        """
        filename = f"{document_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = self.csv_dir / filename
        
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Field Name", "Value", "Confidence", "Source Region"])
            
            for field_name, field in extraction_result.fields.items():
                writer.writerow([
                    field_name,
                    str(field.value),
                    f"{field.confidence:.4f}",
                    field.source_region or ""
                ])
        
        return file_path
    
    def results_to_csv_data(self, extraction_result: ExtractionResult) -> str:
        """
        Convert extraction results to CSV string.
        
        Args:
            extraction_result: Extraction result to convert
            
        Returns:
            CSV string
        """
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Field Name", "Value", "Confidence", "Source Region"])
        
        for field_name, field in extraction_result.fields.items():
            writer.writerow([
                field_name,
                str(field.value),
                f"{field.confidence:.4f}",
                field.source_region or ""
            ])
        
        return output.getvalue()
