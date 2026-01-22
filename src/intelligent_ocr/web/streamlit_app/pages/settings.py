"""Settings page."""

import streamlit as st


def main():
    """Settings page."""
    st.set_page_config(
        page_title="Intelligent OCR - Settings",
        page_icon="⚙️",
        layout="wide"
    )
    
    from intelligent_ocr.web.streamlit_app.components.layout import (
        render_header,
        render_footer
    )
    
    render_header()
    
    st.subheader("⚙️ Settings")
    
    # API Configuration
    st.markdown("### API Configuration")
    api_url = st.text_input(
        "API Base URL",
        value=st.session_state.get("api_url", "http://localhost:8000"),
        help="Base URL of the FastAPI backend"
    )
    st.session_state["api_url"] = api_url
    
    # Test connection
    if st.button("Test Connection"):
        from intelligent_ocr.web.streamlit_app.api_client import APIClient
        client = APIClient(base_url=api_url)
        if client.health_check():
            st.success("✅ Connection successful!")
            try:
                supported = client.get_supported_types()
                st.json(supported)
            except Exception as e:
                st.warning(f"Could not fetch supported types: {str(e)}")
        else:
            st.error("❌ Connection failed. Please check the API URL.")
    
    st.divider()
    
    # Default Settings
    st.markdown("### Default Processing Settings")
    
    document_type = st.selectbox(
        "Default Document Type",
        options=["auto", "form", "cv", "invoice"],
        index=0,
        help="Default document type for processing"
    )
    st.session_state["document_type"] = document_type
    
    language = st.selectbox(
        "Default Language",
        options=["eng", "fra", "ara"],
        index=0,
        help="Default OCR language"
    )
    st.session_state["language"] = language
    
    st.divider()
    
    # About
    st.markdown("### About")
    st.markdown("""
    **Intelligent OCR** is a document processing system that extracts structured data
    from semi-structured documents using OCR and semantic extraction.
    
    **Features:**
    - PDF and image support
    - Text extraction with OCR
    - Semantic field extraction (names, dates, emails, amounts)
    - JSON and CSV export
    """)
    
    render_footer()


if __name__ == "__main__":
    main()
