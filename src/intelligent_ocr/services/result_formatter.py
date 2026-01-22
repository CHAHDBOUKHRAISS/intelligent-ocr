"""Result formatter for converting OCR results to structured formats."""

import json
import csv
import io
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from intelligent_ocr.domain.schemas.ocr import OCRResult
from intelligent_ocr.domain.schemas.layout import LayoutDetectionResult
from intelligent_ocr.domain.schemas.extraction import ExtractionResult
from intelligent_ocr.config.settings import settings


class ResultFormatter:
    """Formatter for OCR results to structured JSON and CSV."""
    
    def __init__(self):
        """Initialize result formatter."""
        self.json_dir = settings.output_json_dir
        self.csv_dir = settings.output_csv_dir
    
    def format_to_json(
        self,
        document_id: str,
        filename: str,
        ocr_result: Optional[OCRResult] = None,
        layout_result: Optional[LayoutDetectionResult] = None,
        extraction_result: Optional[ExtractionResult] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Format all results into structured JSON.
        
        Handles missing fields gracefully by using None or empty values.
        
        Args:
            document_id: Document identifier
            filename: Original filename
            ocr_result: OCR processing result
            layout_result: Layout detection result
            extraction_result: Semantic extraction result
            metadata: Additional metadata
            
        Returns:
            Structured JSON dictionary
        """
        result = {
            "document_id": document_id,
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
            "ocr": self._format_ocr_result(ocr_result) if ocr_result else None,
            "layout": self._format_layout_result(layout_result) if layout_result else None,
            "extraction": self._format_extraction_result(extraction_result) if extraction_result else None,
            "metadata": metadata or {}
        }
        
        return result
    
    def _format_ocr_result(self, ocr_result: OCRResult) -> Dict[str, Any]:
        """Format OCR result to JSON structure."""
        return {
            "full_text": ocr_result.full_text or "",
            "average_confidence": round(ocr_result.average_confidence, 4) if ocr_result.average_confidence else 0.0,
            "text_blocks": [
                {
                    "text": block.text or "",
                    "confidence": round(block.confidence, 4) if block.confidence else 0.0,
                    "bounding_box": {
                        "x": block.bounding_box.x if block.bounding_box else None,
                        "y": block.bounding_box.y if block.bounding_box else None,
                        "width": block.bounding_box.width if block.bounding_box else None,
                        "height": block.bounding_box.height if block.bounding_box else None,
                    } if block.bounding_box else None,
                    "region_id": block.region_id or None
                }
                for block in (ocr_result.blocks or [])
            ],
            "block_count": len(ocr_result.blocks) if ocr_result.blocks else 0
        }
    
    def _format_layout_result(self, layout_result: LayoutDetectionResult) -> Dict[str, Any]:
        """Format layout detection result to JSON structure."""
        return {
            "page_width": layout_result.page_width or 0,
            "page_height": layout_result.page_height or 0,
            "regions": [
                {
                    "region_id": region.region_id or "",
                    "region_type": region.region_type or "",
                    "confidence": round(region.confidence, 4) if region.confidence else 0.0,
                    "bounding_box": {
                        "x": region.bounding_box.x,
                        "y": region.bounding_box.y,
                        "width": region.bounding_box.width,
                        "height": region.bounding_box.height,
                    }
                }
                for region in (layout_result.regions or [])
            ],
            "region_count": len(layout_result.regions) if layout_result.regions else 0
        }
    
    def _format_extraction_result(self, extraction_result: ExtractionResult) -> Dict[str, Any]:
        """Format extraction result to JSON structure."""
        formatted_fields = {}
        
        # Format each extracted field
        for field_name, field in (extraction_result.fields or {}).items():
            formatted_fields[field_name] = {
                "value": field.value,
                "confidence": round(field.confidence, 4) if field.confidence else 0.0,
                "source_region": field.source_region or None
            }
        
        return {
            "fields": formatted_fields,
            "field_count": len(formatted_fields),
            "raw_data": extraction_result.raw_data or {}
        }
    
    def format_to_csv(
        self,
        extraction_result: Optional[ExtractionResult],
        include_ocr: bool = False,
        ocr_result: Optional[OCRResult] = None
    ) -> str:
        """
        Format extraction results to CSV string.
        
        Handles missing fields gracefully.
        
        Args:
            extraction_result: Semantic extraction result
            include_ocr: Whether to include OCR text blocks
            ocr_result: OCR result (required if include_ocr=True)
            
        Returns:
            CSV string
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        headers = ["Field Name", "Value", "Confidence", "Source Region"]
        if include_ocr:
            headers.extend(["OCR Text", "OCR Confidence"])
        writer.writerow(headers)
        
        # Write extraction fields
        if extraction_result and extraction_result.fields:
            for field_name, field in extraction_result.fields.items():
                row = [
                    field_name or "",
                    self._format_value_for_csv(field.value),
                    f"{field.confidence:.4f}" if field.confidence else "0.0000",
                    field.source_region or ""
                ]
                
                if include_ocr and ocr_result:
                    # Find matching OCR block by region_id
                    ocr_text, ocr_conf = self._find_ocr_for_region(
                        field.source_region,
                        ocr_result
                    )
                    row.extend([ocr_text, f"{ocr_conf:.4f}" if ocr_conf else "0.0000"])
                
                writer.writerow(row)
        else:
            # Write empty row if no fields
            row = ["", "", "0.0000", ""]
            if include_ocr:
                row.extend(["", "0.0000"])
            writer.writerow(row)
        
        return output.getvalue()
    
    def _format_value_for_csv(self, value: Any) -> str:
        """Format value for CSV output."""
        if value is None:
            return ""
        elif isinstance(value, (list, tuple)):
            return "; ".join(str(v) for v in value)
        else:
            return str(value)
    
    def _find_ocr_for_region(
        self,
        region_id: Optional[str],
        ocr_result: OCRResult
    ) -> Tuple[str, float]:
        """Find OCR text and confidence for a given region ID."""
        if not region_id or not ocr_result.blocks:
            return "", 0.0
        
        for block in ocr_result.blocks:
            if block.region_id == region_id:
                return block.text or "", block.confidence or 0.0
        
        return "", 0.0
    
    def export_json_file(
        self,
        document_id: str,
        formatted_data: Dict[str, Any]
    ) -> Path:
        """
        Export formatted JSON data to file.
        
        Args:
            document_id: Document identifier
            formatted_data: Formatted JSON data
            
        Returns:
            Path to exported JSON file
        """
        filename = f"{document_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path = self.json_dir / filename
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(formatted_data, f, indent=2, ensure_ascii=False, default=str)
        
        return file_path
    
    def export_csv_file(
        self,
        document_id: str,
        csv_data: str
    ) -> Path:
        """
        Export CSV data to file.
        
        Args:
            document_id: Document identifier
            csv_data: CSV string data
            
        Returns:
            Path to exported CSV file
        """
        filename = f"{document_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = self.csv_dir / filename
        
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            f.write(csv_data)
        
        return file_path
    
    def format_complete_results(
        self,
        document_id: str,
        filename: str,
        ocr_result: Optional[OCRResult] = None,
        layout_result: Optional[LayoutDetectionResult] = None,
        extraction_result: Optional[ExtractionResult] = None,
        metadata: Optional[Dict[str, Any]] = None,
        export_json: bool = True,
        export_csv: bool = False,
        include_ocr_in_csv: bool = False
    ) -> Dict[str, Any]:
        """
        Format complete results and optionally export to files.
        
        Args:
            document_id: Document identifier
            filename: Original filename
            ocr_result: OCR processing result
            layout_result: Layout detection result
            extraction_result: Semantic extraction result
            metadata: Additional metadata
            export_json: Whether to export JSON file
            export_csv: Whether to export CSV file
            include_ocr_in_csv: Whether to include OCR data in CSV
            
        Returns:
            Dictionary with formatted data and export paths
        """
        # Format to JSON structure
        json_data = self.format_to_json(
            document_id=document_id,
            filename=filename,
            ocr_result=ocr_result,
            layout_result=layout_result,
            extraction_result=extraction_result,
            metadata=metadata
        )
        
        result = {
            "json_data": json_data,
            "json_path": None,
            "csv_data": None,
            "csv_path": None
        }
        
        # Export JSON file if requested
        if export_json:
            result["json_path"] = str(self.export_json_file(document_id, json_data))
        
        # Format and export CSV if requested
        if export_csv:
            csv_data = self.format_to_csv(
                extraction_result=extraction_result,
                include_ocr=include_ocr_in_csv,
                ocr_result=ocr_result
            )
            result["csv_data"] = csv_data
            result["csv_path"] = str(self.export_csv_file(document_id, csv_data))
        
        return result
    
    def get_summary(self, formatted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get summary statistics from formatted data.
        
        Args:
            formatted_data: Formatted JSON data
            
        Returns:
            Summary dictionary
        """
        summary = {
            "document_id": formatted_data.get("document_id", ""),
            "filename": formatted_data.get("filename", ""),
            "timestamp": formatted_data.get("timestamp", ""),
        }
        
        # OCR summary
        if formatted_data.get("ocr"):
            ocr = formatted_data["ocr"]
            summary["ocr"] = {
                "has_text": bool(ocr.get("full_text")),
                "text_length": len(ocr.get("full_text", "")),
                "block_count": ocr.get("block_count", 0),
                "average_confidence": ocr.get("average_confidence", 0.0)
            }
        
        # Layout summary
        if formatted_data.get("layout"):
            layout = formatted_data["layout"]
            summary["layout"] = {
                "page_dimensions": {
                    "width": layout.get("page_width", 0),
                    "height": layout.get("page_height", 0)
                },
                "region_count": layout.get("region_count", 0)
            }
        
        # Extraction summary
        if formatted_data.get("extraction"):
            extraction = formatted_data["extraction"]
            summary["extraction"] = {
                "field_count": extraction.get("field_count", 0),
                "fields": list(extraction.get("fields", {}).keys())
            }
        
        return summary
