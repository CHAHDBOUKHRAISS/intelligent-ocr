"""Custom widgets for Streamlit app."""

import streamlit as st
from PIL import Image
import io


def display_image_preview(image_bytes: bytes, filename: str):
    """
    Display image preview.
    
    Args:
        image_bytes: Image file bytes
        filename: Name of the file
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, caption=filename, use_container_width=True)
    except Exception as e:
        st.error(f"Could not display image: {str(e)}")


def display_pdf_preview(file_bytes: bytes, filename: str):
    """
    Display PDF preview (first page as image).
    
    Args:
        file_bytes: PDF file bytes
        filename: Name of the file
    """
    try:
        from pdf2image import convert_from_bytes
        images = convert_from_bytes(file_bytes, first_page=1, last_page=1)
        if images:
            st.image(images[0], caption=f"{filename} (Page 1)", use_container_width=True)
        else:
            st.info("PDF preview not available")
    except Exception as e:
        st.info(f"PDF preview: {str(e)}")


def display_extraction_results(results: dict):
    """
    Display extracted data in a readable format.
    
    Args:
        results: Results dictionary from API
    """
    if not results:
        st.warning("No results to display")
        return
    
    # Display extraction fields
    if "extraction" in results and results["extraction"]:
        extraction = results["extraction"]
        
        if "fields" in extraction and extraction["fields"]:
            st.subheader("📋 Extracted Fields")
            
            fields = extraction["fields"]
            
            cols = st.columns(2)
            
            for idx, (field_name, field_data) in enumerate(fields.items()):
                col = cols[idx % 2]
                
                with col:
                    value = field_data.get("value", "")
                    confidence = field_data.get("confidence", 0.0)
                    
                    display_name = field_name.replace("_", " ").title()
                    
                    st.markdown(f"**{display_name}**")
                    if isinstance(value, list):
                        st.write(", ".join(str(v) for v in value))
                    else:
                        st.write(str(value))
                    
                    confidence_color = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.5 else "🔴"
                    st.caption(f"{confidence_color} Confidence: {confidence:.1%}")
                    st.divider()
        else:
            st.info("No fields extracted")
    
    # Display OCR text
    if "ocr" in results and results["ocr"]:
        ocr = results["ocr"]
        
        if ocr.get("full_text"):
            with st.expander("📝 Full OCR Text", expanded=False):
                st.text_area(
                    "Extracted Text",
                    value=ocr.get("full_text", ""),
                    height=200,
                    disabled=True,
                    label_visibility="collapsed"
                )
                
                # OCR statistics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Text Blocks", ocr.get("block_count", 0))
                with col2:
                    st.metric("Avg Confidence", f"{ocr.get('average_confidence', 0):.1%}")


def create_download_button(data: dict, filename: str, format_type: str = "json"):
    """
    Create download button for results.
    
    Args:
        data: Data to download
        filename: Base filename
        format_type: Format type (json or csv)
    """
    import json
    
    if format_type == "json":
        file_data = json.dumps(data, indent=2, ensure_ascii=False, default=str)
        mime_type = "application/json"
        file_extension = "json"
    else:
        # CSV format
        file_data = data.get("csv_data", "")
        mime_type = "text/csv"
        file_extension = "csv"
    
    st.download_button(
        label=f"⬇️ Download {format_type.upper()}",
        data=file_data,
        file_name=f"{filename}_{format_type}.{file_extension}",
        mime=mime_type,
        use_container_width=True
    )
