"""Document processing endpoints."""

import io
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, Response
from typing import Optional

from intelligent_ocr.domain.enums import DocumentType, OutputFormat, ProcessingStatus
from intelligent_ocr.domain.schemas.document import DocumentUpload, DocumentMetadata
from intelligent_ocr.core.utils import generate_document_id
from intelligent_ocr.core.exceptions import FileValidationError, OCRPipelineError
from intelligent_ocr.api.deps import (
    get_document_service,
    get_export_service,
    get_storage_service
)
from intelligent_ocr.services.document_service import DocumentService
from intelligent_ocr.services.export_service import ExportService
from intelligent_ocr.services.storage_service import StorageService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentMetadata)
async def upload_document(
    file: UploadFile = File(...),
    document_type: DocumentType = Query(default=DocumentType.AUTO, description="Document type"),
    language: str = Query(default="eng", description="OCR language code"),
    document_service: DocumentService = Depends(get_document_service),
    storage_service: StorageService = Depends(get_storage_service)
):
    """
    Upload and process a document.
    
    Supports images (jpg, png, tiff, etc.) and PDF files.
    """
    # Validate file
    try:
        file_content = await file.read()
        file_size = len(file_content)
        
        document_service.validate_file(file.filename, file_size)
    except FileValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Generate document ID
    document_id = generate_document_id()
    
    # Save file
    file_obj = io.BytesIO(file_content)
    try:
        file_path = storage_service.save_uploaded_file(
            file=file_obj,
            filename=file.filename,
            document_id=document_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Create metadata
    metadata = document_service.create_metadata(
        document_id=document_id,
        filename=file.filename,
        file_size=file_size,
        document_type=document_type,
        status=ProcessingStatus.PROCESSING
    )
    
    return metadata


@router.post("/{document_id}/process")
async def process_document(
    document_id: str,
    language: str = Query(default="eng", description="OCR language code"),
    document_service: DocumentService = Depends(get_document_service),
    storage_service: StorageService = Depends(get_storage_service),
    export_service: ExportService = Depends(get_export_service)
):
    """
    Process a previously uploaded document through OCR pipeline.
    
    Returns JSON results by default.
    """
    # Find the uploaded file
    # In a real implementation, you'd track this in a database
    # For now, we'll search for files in the upload directory
    upload_dir = storage_service.upload_dir / document_id
    if not upload_dir.exists():
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Find the first file in the document directory
    files = list(upload_dir.glob("*"))
    if not files:
        raise HTTPException(status_code=404, detail="No file found for document")
    
    file_path = files[0]
    
    # Detect document type from filename
    document_type = document_service.detect_document_type(file_path.name)
    
    # Process document
    try:
        results = document_service.process_document(
            file_path=file_path,
            document_type=document_type,
            language=language
        )
        
        # Add document ID to results
        results["document_id"] = document_id
        results["filename"] = file_path.name
        
        # Export JSON
        json_path = export_service.export_json(document_id, results)
        results["json_export_path"] = str(json_path)
        
        # Export CSV if extraction results exist
        if "extraction" in results and results["extraction"]:
            from intelligent_ocr.domain.schemas.extraction import ExtractionResult
            extraction = ExtractionResult(**results["extraction"])
            if extraction.fields:
                csv_path = export_service.export_csv(document_id, extraction)
                results["csv_export_path"] = str(csv_path)
        
        return JSONResponse(content=results)
    except OCRPipelineError as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.post("/upload-and-process")
async def upload_and_process(
    file: UploadFile = File(...),
    document_type: DocumentType = Query(default=DocumentType.AUTO, description="Document type"),
    language: str = Query(default="eng", description="OCR language code"),
    output_format: OutputFormat = Query(default=OutputFormat.JSON, description="Output format"),
    document_service: DocumentService = Depends(get_document_service),
    storage_service: StorageService = Depends(get_storage_service),
    export_service: ExportService = Depends(get_export_service)
):
    """
    Upload and process document in a single request.
    
    Returns extracted data as JSON or CSV.
    """
    # Validate and save file
    try:
        file_content = await file.read()
        file_size = len(file_content)
        document_service.validate_file(file.filename, file_size)
    except FileValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    document_id = generate_document_id()
    file_obj = io.BytesIO(file_content)
    
    try:
        file_path = storage_service.save_uploaded_file(
            file=file_obj,
            filename=file.filename,
            document_id=document_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Detect document type if AUTO
    if document_type == DocumentType.AUTO:
        document_type = document_service.detect_document_type(file.filename)
    
    # Process document
    try:
        results = document_service.process_document(
            file_path=file_path,
            document_type=document_type,
            language=language
        )
        
        results["document_id"] = document_id
        results["filename"] = file.filename
        
        # Handle output format
        if output_format == OutputFormat.CSV:
            # Export CSV
            if "extraction" in results and results["extraction"]:
                from intelligent_ocr.domain.schemas.extraction import ExtractionResult
                extraction = ExtractionResult(**results["extraction"])
                csv_data = export_service.results_to_csv_data(extraction)
                
                return Response(
                    content=csv_data,
                    media_type="text/csv",
                    headers={
                        "Content-Disposition": f"attachment; filename={document_id}_results.csv"
                    }
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="No extraction results available for CSV export"
                )
        else:
            # Return JSON
            json_path = export_service.export_json(document_id, results)
            results["json_export_path"] = str(json_path)
            
            return JSONResponse(content=results)
    
    except OCRPipelineError as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.get("/{document_id}/results")
async def get_results(
    document_id: str,
    output_format: OutputFormat = Query(default=OutputFormat.JSON, description="Output format"),
    export_service: ExportService = Depends(get_export_service)
):
    """
    Get processing results for a document.
    
    Returns JSON or CSV based on output_format parameter.
    """
    # In a real implementation, you'd load results from database or cache
    # For now, search for JSON file
    json_files = list(export_service.json_dir.glob(f"{document_id}_*.json"))
    
    if not json_files:
        raise HTTPException(status_code=404, detail="Results not found")
    
    import json
    with open(json_files[0], "r", encoding="utf-8") as f:
        results = json.load(f)
    
    if output_format == OutputFormat.CSV:
        if "extraction" in results and results["extraction"]:
            from intelligent_ocr.domain.schemas.extraction import ExtractionResult
            extraction = ExtractionResult(**results["extraction"])
            csv_data = export_service.results_to_csv_data(extraction)
            
            return Response(
                content=csv_data,
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename={document_id}_results.csv"
                }
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="No extraction results available for CSV export"
            )
    else:
        return JSONResponse(content=results)
