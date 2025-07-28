import streamlit as st
import base64
from pathlib import Path

#######################################################################################################################################
# Page Configuration and Formatting
#######################################################################################################################################

st.set_page_config(
    page_title="QAP 2024-2025 Documentation - LIHTC Scoring Tool",
    layout="wide"
)

# Apply consistent styling from main app
st.markdown("""
    <style>
        /* === Global Defaults === */
        * {
            border-radius: 4px !important;
        }

        /* === Input Styling === */
        .stButton > button,
        .stTextInput > div > div,
        .stSelectbox > div,
        .stSlider > div,
        .stCheckbox > div,
        .stRadio > div,
        .stForm,
        .stDataFrame,
        .stMetric {
            border-radius: 4px !important;
        }

        /* === Label Styling for All Common Form Inputs === */
        div[data-testid="stTextInput"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stCheckbox"] label,
        div[data-testid="stSlider"] label,
        div[data-testid="stRadio"] label {
            font-size: 16px !important;
            font-weight: 500 !important;
            color: #222 !important;
        }

        /* === PDF Viewer Styling === */
        .pdf-container {
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 10px 0;
            background-color: #f9f9f9;
        }

        /* === Download Button Styling === */
        .download-button {
            background-color: #2B2D42;
            color: white;
            padding: 12px 24px;
            border-radius: 4px;
            text-decoration: none;
            display: inline-block;
            margin: 10px 5px;
            font-weight: 500;
            transition: background-color 0.3s;
        }

        .download-button:hover {
            background-color: #1a1c2e;
            color: white;
            text-decoration: none;
        }

        /* === Info Box Styling === */
        .info-box {
            background-color: #e8f4fd;
            border-left: 4px solid #2B2D42;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
        }
    </style>
""", unsafe_allow_html=True)

#######################################################################################################################################
# Helper Functions
#######################################################################################################################################

@st.cache_data
def load_qap_pdf():
    """Load the QAP 2024-2025 PDF file"""
    pdf_path = Path("QAP2024_2025.pdf")
    
    if pdf_path.exists():
        return pdf_path
    return None

def display_pdf(file_path):
    """Display PDF in Streamlit using base64 encoding"""
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        pdf_display = f"""
        <div class="pdf-container">
            <embed src="data:application/pdf;base64,{base64_pdf}" 
                   width="100%" 
                   height="800px" 
                   type="application/pdf"
                   style="border-radius: 4px;">
        </div>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
        return True
    except Exception as e:
        st.error(f"Error loading PDF: {str(e)}")
        return False

def create_download_link(file_path):
    """Create a download link for the QAP PDF"""
    try:
        with open(file_path, "rb") as f:
            pdf_data = f.read()
        
        b64_pdf = base64.b64encode(pdf_data).decode()
        download_link = f"""
        <a href="data:application/pdf;base64,{b64_pdf}" 
           download="QAP2024_2025.pdf" 
           class="download-button">
           Download QAP 2024-2025
        </a>
        """
        return download_link
    except Exception as e:
        st.error(f"Error creating download link: {str(e)}")
        return None

#######################################################################################################################################
# Main Page Content
#######################################################################################################################################

st.title("Qualified Allocation Plan (QAP) 2024-2025")

# Load the QAP PDF
qap_pdf_path = load_qap_pdf()

if qap_pdf_path:
    # Main layout
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>About This Document</h4>
            <p>The Qualified Allocation Plan (QAP) provides the framework and criteria for allocating 
            Low-Income Housing Tax Credits (LIHTC). This document contains the official scoring 
            methodologies and requirements that this tool implements.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display the PDF
        if display_pdf(qap_pdf_path):
            st.success("QAP Document loaded successfully")
        
    with col2:
        st.subheader("Document Details")
        
        # File information
        file_size = qap_pdf_path.stat().st_size / 1024 / 1024  # Size in MB
        st.metric("File Size", f"{file_size:.2f} MB")
        st.metric("Document", "QAP 2024-2025")
        
        # Download button
        download_link = create_download_link(qap_pdf_path)
        if download_link:
            st.markdown(download_link, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick navigation
        st.subheader("Quick Navigation")
        st.markdown("""
        **Key Sections:**
        - Location Scoring Criteria
        - Community Transportation
        - Desirable/Undesirable Activities
        - Quality Education Standards
        - Stable Communities Indicators
        - Scoring Methodology
        """)
        
        st.markdown("---")
        
        # Related tools
        st.subheader("Related Tools")
        if st.button("Back to Scoring Tool"):
            st.switch_page("Scoring_Tool.py")
        
        if st.button("View Location Maps"):
            st.info("Navigate to the main tool to access location maps")
        
        st.markdown("---")
        
        # Document status
        st.subheader("Document Status")
        st.success("Current Version")
        st.info("Valid: 2024-2025")
        
else:
    # Error handling if PDF not found
    st.error("QAP 2024-2025 PDF file not found")
    st.markdown("""
    ### Expected File Location:
    `QAP2024_2025.pdf`
    
    ### Troubleshooting:
    1. **Check file exists** - Verify the PDF file is in the correct location
    2. **Check file permissions** - Ensure the file is readable
    3. **Check file name** - Verify the filename matches exactly: `QAP2024_2025.pdf`
    
    ### Alternative Actions:
    """)
    
    # File upload as backup
    st.subheader("Upload QAP Document")
    uploaded_file = st.file_uploader(
        "Upload the QAP 2024-2025 PDF file",
        type=['pdf'],
        help="Upload the QAP document if it's not found in the expected location"
    )
    
    if uploaded_file is not None:
        # Display uploaded file
        try:
            pdf_data = uploaded_file.read()
            base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            
            pdf_display = f"""
            <div class="pdf-container">
                <embed src="data:application/pdf;base64,{base64_pdf}" 
                       width="100%" 
                       height="800px" 
                       type="application/pdf"
                       style="border-radius: 4px;">
            </div>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)
            st.success("Uploaded QAP document displayed successfully")
            
        except Exception as e:
            st.error(f"Error displaying uploaded PDF: {str(e)}")

#######################################################################################################################################
# Footer with navigation
#######################################################################################################################################

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 14px; padding: 20px;'>
    <strong>LIHTC Scoring Tool - QAP Documentation</strong><br>
    Qualified Allocation Plan 2024-2025 | 
    <a href="/" style="color: #2B2D42; text-decoration: none;">Back to Main Scoring Tool</a>
</div>
""", unsafe_allow_html=True)

# Additional information section
with st.expander("How to Use This Document"):
    st.markdown("""
    ### Navigation Tips:
    - **Zoom**: Use your browser's zoom controls (Ctrl/Cmd + or -)
    - **Search**: Use Ctrl/Cmd + F to search within the document
    - **Download**: Click the download button to save a local copy
    
    ### Key Information:
    - This document contains the official LIHTC allocation criteria
    - Location scoring methodologies are detailed in specific sections
    - Use this as reference when understanding scoring results
    
    ### Technical Notes:
    - The scoring tool implements the methodologies outlined in this QAP
    - All calculations follow the standards specified in this document
    - For discrepancies, this QAP document is the authoritative source
    """)