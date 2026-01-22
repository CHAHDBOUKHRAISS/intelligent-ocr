"""Main page for uploading and processing documents."""

import streamlit as st
import io
from intelligent_ocr.web.streamlit_app.api_client import APIClient
from intelligent_ocr.web.streamlit_app.components.widgets import (
    display_image_preview,
    display_pdf_preview,
    display_extraction_results,
    create_download_button
)


def main():
    """Main upload and OCR page."""
    st.set_page_config(
        page_title="Intelligent OCR - Upload",
        page_icon="🔍",
        layout="wide"
    )
    
    from intelligent_ocr.web.streamlit_app.components.layout import (
        render_header,
        render_sidebar,
        render_footer
    )
    
    render_header()
    render_sidebar()
    
    # Initialize session state
    if "results" not in st.session_state:
        st.session_state.results = None
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Document")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "png", "jpg", "jpeg", "tiff", "tif", "bmp", "webp"],
            help="Upload a PDF or image file"
        )
        
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            
            # Display file info
            file_details = {
                "Filename": uploaded_file.name,
                "File Type": uploaded_file.type,
                "File Size": f"{uploaded_file.size / 1024:.2f} KB"
            }
            st.json(file_details)
            
            # Display preview
            st.subheader("👁️ Preview")
            file_bytes = uploaded_file.read()
            uploaded_file.seek(0)  # Reset file pointer
            
            if uploaded_file.type == "application/pdf":
                display_pdf_preview(file_bytes, uploaded_file.name)
            else:
                display_image_preview(file_bytes, uploaded_file.name)
            
            # Process button
            st.divider()
            if st.button("🚀 Process Document", type="primary", use_container_width=True):
                process_document(uploaded_file)
    
    with col2:
        st.subheader("📊 Results")
        
        if st.session_state.results:
            display_results(st.session_state.results)
        else:
            st.info("👈 Upload a document and click 'Process Document' to see results")
    
    render_footer()


def process_document(uploaded_file):
    """Process uploaded document through API."""
    api_url = st.session_state.get("api_url", "http://localhost:8000")
    document_type = st.session_state.get("document_type", "auto")
    language = st.session_state.get("language", "eng")
    
    client = APIClient(base_url=api_url)
    
    # Check API connection
    if not client.health_check():
        st.error("❌ Cannot connect to API. Please check the API URL in settings.")
        return
    
    # Show progress
    with st.spinner("Processing document..."):
        try:
            # Read file bytes
            file_bytes = uploaded_file.read()
            file_obj = io.BytesIO(file_bytes)
            
            # Upload and process
            results = client.upload_and_process(
                file=file_obj,
                filename=uploaded_file.name,
                document_type=document_type,
                language=language,
                output_format="json"
            )
            
            st.session_state.results = results
            st.success("✅ Document processed successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")


def display_results(results: dict):
    """Display processing results."""
    if not results:
        st.warning("No results available")
        return
    
    # Display extraction results
    display_extraction_results(results)
    
    # Download buttons
    st.divider()
    st.subheader("💾 Download Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON download
        if "extraction" in results or "ocr" in results:
            create_download_button(results, "ocr_results", "json")
    
    with col2:
        # CSV download (if available)
        if "csv_data" in results:
            create_download_button(results, "ocr_results", "csv")
        else:
            # Try to get CSV version
            st.info("Request CSV format for CSV download")


if __name__ == "__main__":
    main()
