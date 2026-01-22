"""Layout components for Streamlit app."""

import streamlit as st


def render_header():
    """Render app header."""
    st.title("🔍 Intelligent OCR")
    st.markdown("**Extract structured data from documents using OCR and AI**")
    st.divider()


def render_sidebar():
    """Render sidebar with settings."""
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API URL configuration
        api_url = st.text_input(
            "API URL",
            value=st.session_state.get("api_url", "http://localhost:8000"),
            help="URL of the FastAPI backend"
        )
        st.session_state["api_url"] = api_url
        
        # Check API connection
        if st.button("Check Connection", use_container_width=True):
            from intelligent_ocr.web.streamlit_app.api_client import APIClient
            client = APIClient(base_url=api_url)
            if client.health_check():
                st.success("✅ Connected")
            else:
                st.error("❌ Connection failed")
        
        st.divider()
        
        # Document type selection
        document_type = st.selectbox(
            "Document Type",
            options=["auto", "form", "cv", "invoice"],
            index=0,
            help="Type of document to process"
        )
        st.session_state["document_type"] = document_type
        
        # Language selection
        language = st.selectbox(
            "Language",
            options=["eng", "fra", "ara"],
            index=0,
            help="OCR language"
        )
        st.session_state["language"] = language
        
        st.divider()
        
        st.markdown("### 📖 About")
        st.markdown("""
        Upload a document (PDF or image) to extract:
        - Text content
        - Names, dates, emails
        - Monetary amounts
        - Structured data
        """)


def render_footer():
    """Render app footer."""
    st.divider()
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Intelligent OCR - Document Processing System</div>",
        unsafe_allow_html=True
    )
