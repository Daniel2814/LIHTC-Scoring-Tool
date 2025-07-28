import streamlit as st
from pathlib import Path

#######################################################################################################################################
# Page Configuration and Formatting
#######################################################################################################################################

st.set_page_config(
    page_title="About LIHTC Scoring Tool",
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

        /* === Info Box Styling === */
        .info-box {
            background-color: #f8f9fa;
            border-left: 4px solid #2B2D42;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }

        .highlight-box {
            background-color: #e8f4fd;
            border: 1px solid #2B2D42;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }

        .feature-card {
            background-color: #ffffff;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* === Navigation Button Styling === */
        .nav-button {
            background-color: #2B2D42;
            color: white;
            padding: 12px 24px;
            border-radius: 4px;
            text-decoration: none;
            display: inline-block;
            margin: 10px 5px;
            font-weight: 500;
            transition: background-color 0.3s;
            text-align: center;
        }

        .nav-button:hover {
            background-color: #1a1c2e;
            color: white;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)

#######################################################################################################################################
# Main Page Content
#######################################################################################################################################

st.title("About the LIHTC Scoring Tool")

# Hero section
st.markdown("""
<div class="highlight-box">
    <h3>Empowering Small Developers with Data-Driven Insights</h3>
    <p style="font-size: 18px; margin-bottom: 0;">
        A comprehensive tool designed to help smaller developers assess the feasibility 
        of obtaining Low-Income Housing Tax Credits (LIHTC) from the government.
    </p>
</div>
""", unsafe_allow_html=True)

# Main content in columns
col1, col2 = st.columns([2, 1])

with col1:
    # What is LIHTC section
    st.header("What is LIHTC?")
    
    st.markdown("""
    <div class="info-box">
        <h4>Low-Income Housing Tax Credit Program</h4>
        <p>
            The Low-Income Housing Tax Credit (LIHTC) is a federal program designed to 
            incentivize the development and rehabilitation of affordable rental housing 
            across the United States. Established in 1986, it has become the nation's 
            primary tool for creating affordable housing.
        </p>
        <p>
            The program provides tax credits to developers who agree to rent a certain 
            portion of their housing units to low-income households at below-market rates 
            for a minimum of 30 years.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Why this tool exists
    st.header("Why This Tool Exists")
    
    st.markdown("""
    ### The Challenge
    
    Small developers often lack the resources and expertise to effectively compete 
    with large corporations for tax credits. The allocation process is complex and 
    highly competitive, with government tax credits awarded based on:
    
    - **Location characteristics** - Community quality, transportation access, education
    - **Developer qualifications** - Experience, financial capacity, track record
    - **Project design** - Sustainability, amenities, community impact
    
    ### The Solution
    
    This scoring tool levels the playing field by providing small developers with 
    the same analytical capabilities that large firms use to evaluate potential projects. 
    The better planned and more liveable your proposed development location, the higher 
    your competitive advantage in the LIHTC allocation process.
    """)

    # How it works
    st.header("How the Tool Works")
    
    features = [
        {
            "title": "Location Analysis",
            "description": "Comprehensive scoring of transportation, education, and community amenities"
        },
        {
            "title": "Competitive Assessment", 
            "description": "Compare your proposed site against successful applications in the region"
        },
        {
            "title": "Data Visualization",
            "description": "Interactive maps and charts to understand location advantages and challenges"
        },
        {
            "title": "QAP Compliance",
            "description": "Alignment with Georgia's Qualified Allocation Plan scoring criteria"
        }
    ]
    
    for feature in features:
        st.markdown(f"""
        <div class="feature-card">
            <h5>{feature['title']}</h5>
            <p>{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # Development team info
    st.header("Development Team")
    
    st.markdown("""
    <div class="info-box">
        <h4>Emory University Students</h4>
        <p>
            This tool was developed by students at Emory University as part of an 
            initiative to support equitable housing development and provide accessible 
            technology solutions for smaller developers.
        </p>
        <p>
            <strong>Mission:</strong> Democratize access to housing development insights 
            and support the creation of affordable housing in underserved communities.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tool capabilities
    st.subheader("Tool Capabilities")
    
    capabilities = [
        "Location scoring for 4 key criteria",
        "Interactive mapping interface", 
        "Historical application analysis",
        "Competitive benchmarking",
        "QAP documentation access",
        "Export and reporting features"
    ]
    
    for capability in capabilities:
        st.markdown(f"✓ {capability}")

# Success stories section
st.header("Success Through Strategic Planning")

st.markdown("""
### Why Location Matters

The LIHTC program prioritizes developments that:

- **Enhance community access** to jobs, services, and transportation
- **Promote educational opportunities** through proximity to quality schools
- **Support resident well-being** with access to healthcare and amenities
- **Avoid environmental hazards** and undesirable land uses
- **Strengthen community stability** through thoughtful site selection

### Making Informed Decisions

This tool helps you identify the strongest locations for your affordable housing 
proposals by providing the same data and analysis methods used by successful 
developers and state allocation agencies.
""")

# Call to action
st.markdown("---")

st.markdown("""
<div class="highlight-box">
    <h3>Ready to Get Started?</h3>
    <p>
        Use the LIHTC Scoring Tool to evaluate your potential development sites 
        and improve your competitive position in the tax credit allocation process.
    </p>
</div>
""", unsafe_allow_html=True)

# Navigation buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Start Scoring Tool", use_container_width=True):
        st.switch_page("Scoring_Tool.py")

with col2:
    if st.button("View QAP Documentation", use_container_width=True):
        st.switch_page("pages/QAP_Documentation.py")

with col3:
    if st.button("Scoring Criteria", use_container_width=True):
        st.switch_page("pages/QAP_Criteria.py")

#######################################################################################################################################
# Additional Resources
#######################################################################################################################################

with st.expander("Additional Resources"):
    st.markdown("""
    ### Learn More About LIHTC
    
    - **HUD LIHTC Database**: Search existing LIHTC properties nationwide
    - **State Allocation Agencies**: Find your state's QAP and application process
    - **LIHTC Training**: Professional development courses for developers
    - **Advocacy Organizations**: National Low Income Housing Coalition and similar groups
    
    ### Technical Documentation
    
    - **Data Sources**: Census Bureau, Department of Education, Environmental agencies
    - **Methodology**: Based on Georgia QAP 2024-2025 scoring criteria
    - **Updates**: Tool updated annually to reflect current QAP requirements
    - **Support**: Contact Emory Center for AI for technical assistance
    """)

#######################################################################################################################################
# Footer
#######################################################################################################################################

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 14px; padding: 20px;'>
    <strong>LIHTC Scoring Tool</strong><br>
    Developed by Students at Emory University | 
    <a href="/" style="color: #2B2D42; text-decoration: none;">Return to Scoring Tool</a>
</div>
""", unsafe_allow_html=True)
