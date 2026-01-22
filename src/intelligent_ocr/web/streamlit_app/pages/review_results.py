"""Page for reviewing and managing results."""

import streamlit as st
from intelligent_ocr.web.streamlit_app.components.widgets import (
    display_extraction_results,
    create_download_button
)


def main():
    """Review results page."""
    st.set_page_config(
        page_title="Intelligent OCR - Results",
        page_icon="📊",
        layout="wide"
    )
    
    from intelligent_ocr.web.streamlit_app.components.layout import (
        render_header,
        render_sidebar,
        render_footer
    )
    
    render_header()
    render_sidebar()
    
    st.subheader("📊 Review Results")
    
    if "results" in st.session_state and st.session_state.results:
        display_extraction_results(st.session_state.results)
        
        st.divider()
        st.subheader("💾 Download Results")
        
        col1, col2 = st.columns(2)
        with col1:
            create_download_button(st.session_state.results, "ocr_results", "json")
        with col2:
            if "csv_data" in st.session_state.results:
                create_download_button(st.session_state.results, "ocr_results", "csv")
    else:
        st.info("No results available. Please process a document first.")
    
    render_footer()


if __name__ == "__main__":
    main()
