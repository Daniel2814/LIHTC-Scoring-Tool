import streamlit as st
import pandas as pd

#######################################################################################################################################
# Page Configuration and Formatting
#######################################################################################################################################

st.set_page_config(
    page_title="QAP Criteria - LIHTC Scoring Tool",
    page_icon="📋",
    layout="wide"
)

# Apply minimal consistent styling
st.markdown("""
    <style>
        /* === Global Defaults === */
        * {
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
    </style>
""", unsafe_allow_html=True)

#######################################################################################################################################
# Main Page Content
#######################################################################################################################################

st.title("📋 Georgia DCA LIHTC Scoring Criteria Summary")

# Introduction using standard Streamlit info box
st.info("""
📖 **About the QAP Scoring Criteria**

The Georgia Department of Community Affairs (DCA) uses a comprehensive scoring system to evaluate Low-Income Housing Tax Credit (LIHTC) applications. This page provides a complete overview of all scoring categories and their maximum point values.

📍 **Location-Based Criteria:** The highlighted sections below are the location-based criteria that this scoring tool calculates automatically based on latitude and longitude coordinates.
""")

# Create the criteria data as a DataFrame
criteria_data = {
    "Category": [
        "Extended Affordability Commitment",
        "Minority- & Women-Owned Business", 
        "Favorable Financing",
        "Compliance Performance",
        "Integrated Supportive Housing",
        "Readiness to Proceed",
        "Deeper Rent Targeting / PBRA",
        "HCV & PHA Notices",
        "🎯 Desirable/Undesirable Activities",
        "🎯 Community Transportation Options",
        "🎯 Quality Education Areas", 
        "Revitalization / Redevelopment Plans",
        "🎯 Stable Communities",
        "Community Designations",
        "Phased Development",
        "Previous Projects", 
        "Housing Needs Characteristics",
        "Economic Development Proximity",
        "Mixed-Income Developments",
        "Historic Preservation",
        "Enriched Property Services",
        "DCA Community Initiatives",
        "Preservation Scoring (Rehab Only)"
    ],
    "Max Points": [
        6, 2, 5, 10, 5, 13, 3, 2, "±20", 6, 3, 10, 10, 10, 4, 5, 10, 1, 1, 2, 2, 2, 62
    ],
    "Description": [
        "Waive Qualified Contract (up to 5 pts) + ROFR (+1 pt) or Resident-ownership plan (+1 pt)",
        "Either 10% spend on MWBE (audited) or MWBE team ownership (≥15%)",
        "Combine cheap funding (≤4 pts) + property-cost reduction (≤1 pt)",
        "Start at 10 pts; subtract for SAEs/ACs, add back for good track record",
        "Mix of referrals, PBRA, tenant prefs, and prior performance",
        "Shovel-readiness: zoning, permits, site plans, financing docs",
        "AMI avg ≤58% (2 pts) or ≥20% units with ≥10-yr PBRA (3 pts)",
        "Register as Section 8 landlord + notify local PHAs",
        "Score for proximity to amenities or hazards (net effect)",
        "TOD proximity (up to 6 pts) or fixed-route transit access (up to 3 pts)",
        "Points for schools with high CCRPI/BTO performance in attendance zone",
        "Inside active CRP areas + planning best practices + partner investment",
        "Based on tract indicators (poverty, income, transit, jobs, env. health)",
        "Purpose-Built or HUD CNI-anchored applications only",
        "For 2nd/3rd phase of prior LIHTC development in past 6 QAPs",
        "Rewards counties/tracts with few/no recent awards",
        "For high-need, high-growth tracts (non-Atlanta Metro)",
        "Near major new job-creating projects (≥90 or ≥250 jobs)",
        "Include market-rate units or elect income-averaging",
        "Rehab certified historic structures using HTC equity",
        "CORES-certified GP or 3rd-party service coordinator",
        "Inside GICH area with formal support letter",
        "Based on occupancy, rent gap, age, LURC, site, USDA risk"
    ]
}

# Create DataFrame
df = pd.DataFrame(criteria_data)

st.subheader("📊 Complete Scoring Criteria")

# Note about location-based criteria
st.warning("🎯 **Location-Based Criteria** (marked with target emoji) are automatically calculated by this tool based on your coordinates.")

# Display the table using Streamlit's native dataframe display
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Category": st.column_config.TextColumn(
            "Category",
            width="medium",
        ),
        "Max Points": st.column_config.TextColumn(
            "Max Points",
            width="small",
        ),
        "Description": st.column_config.TextColumn(
            "Description",
            width="large",
        ),
    }
)

# Key statistics using Streamlit metrics
st.subheader("📊 Key Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🎯 Location-Based Points",
        value="39",
        help="Maximum points available from location-based criteria calculated by this tool (20+6+3+10)"
    )

with col2:
    st.metric(
        label="📈 Total Standard Points", 
        value="99",
        help="Total possible points for new construction projects (excluding 62-point preservation scoring)"
    )

with col3:
    st.metric(
        label="📍 Location Impact",
        value="39.4%",
        help="Percentage of total score determined by location criteria"
    )

# Location criteria breakdown
st.subheader("🎯 Location-Based Criteria Details")

# Create tabs for each location criterion
tab1, tab2, tab3, tab4 = st.tabs([
    "Desirable/Undesirable (±20)", 
    "Transportation (6)", 
    "Education (3)", 
    "Stable Communities (10)"
])

with tab1:
    st.markdown("### Desirable/Undesirable Activities (±20 points)")
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("**➕ Desirable Activities:**")
        st.write("• Proximity to grocery stores")
        st.write("• Healthcare facilities")
        st.write("• Community centers")
        st.write("• Parks and recreation")
        st.write("• Public libraries")
    
    with col2:
        st.error("**➖ Undesirable Activities:**")
        st.write("• Environmental hazards")
        st.write("• Industrial sites")
        st.write("• Landfills")
        st.write("• Heavy traffic areas")
        st.write("• Contaminated sites")
    
    st.info("**Net Effect:** Final score can be positive or negative based on the balance of nearby activities")

with tab2:
    st.markdown("### Community Transportation Options (6 points)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("**🚇 Transit-Oriented Development**")
        st.write("• Up to 6 points")
        st.write("• Proximity to major transit hubs")
        st.write("• Rail stations")
        st.write("• Bus rapid transit")
    
    with col2:
        st.info("**🚌 Fixed-Route Transit**")
        st.write("• Up to 3 points")
        st.write("• Regular bus routes")
        st.write("• Scheduled service")
        st.write("• Rural area alternatives")

with tab3:
    st.markdown("### Quality Education Areas (3 points)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("**📊 CCRPI Scores**")
        st.write("• Georgia's school performance index")
        st.write("• Academic achievement metrics")
        st.write("• School improvement indicators")
    
    with col2:
        st.info("**🎯 Beat the Odds (BTO)**")
        st.write("• Recognition for improving schools")
        st.write("• Overperforming expectations")
        st.write("• Must be in attendance zone")

with tab4:
    st.markdown("### Stable Communities (10 points)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("**📈 Positive Indicators**")
        st.write("• Lower poverty rates")
        st.write("• Higher median income")
        st.write("• Good transit access")
        st.write("• Job opportunities nearby")
    
    with col2:
        st.info("**🌍 Environmental Health**")
        st.write("• Air quality measures")
        st.write("• Environmental safety")
        st.write("• Health risk factors")
        st.write("• Community wellness")

# Important notes in expandable sections
with st.expander("ℹ️ Important Notes About Scoring"):
    st.markdown("""
    ### Key Points to Remember:
    
    **📋 Application-Specific Criteria:**
    - **Preservation Scoring (62 pts):** Only applies to rehabilitation projects
    - **Community Designations (10 pts):** Only for Purpose-Built or HUD CNI applications  
    - **Housing Needs Characteristics (10 pts):** For non-Atlanta Metro areas only
    
    **🔄 Variable Scoring:**
    - **Compliance Performance:** Starts at 10 points, can be reduced for violations
    - **Desirable/Undesirable:** Can result in positive or negative net scores
    
    **📚 Additional Information:**
    - See the complete QAP document for detailed eligibility requirements
    - Some criteria have complex sub-scoring methodologies
    - Geographic restrictions apply to certain categories
    """)

with st.expander("🎯 Scoring Strategy Tips"):
    st.markdown("""
    ### Maximizing Location Scores:
    
    **🏆 High-Impact Strategies:**
    1. **Choose Transit-Rich Areas:** 6 points available from transportation proximity
    2. **Target Stable Communities:** 10 points from socioeconomic indicators  
    3. **Avoid Hazards:** Minimize negative impacts from undesirable activities
    4. **Research School Zones:** 3 points available from education quality
    
    **📍 Site Selection Considerations:**
    - Use this tool to compare multiple potential sites
    - Consider the full ±20 point swing from desirable/undesirable activities
    - Balance location scores with other QAP criteria
    - Review maps to understand spatial patterns
    
    **⚖️ Trade-off Analysis:**
    - Location criteria represent ~39% of total possible points
    - Strong location scores can offset weaker areas in other criteria
    - Consider development costs vs. scoring benefits
    """)

# Navigation section
st.markdown("---")
st.subheader("🔗 Related Tools and Documentation")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Calculate Location Scores", type="primary", use_container_width=True):
        st.switch_page("scoring_tool.py")

with col2:
    if st.button("📄 View Full QAP Document", use_container_width=True):
        st.switch_page("pages/QAP_pdf_st.py")

with col3:
    st.info("""
    **📖 Quick Reference:**
    - Location criteria = 39 max points
    - Standard total = 99 points  
    - Location impact = 39.4% of score
    """)

# Footer
st.markdown("---")
st.caption("**Georgia DCA LIHTC Scoring Criteria** | Based on the 2024-2025 Qualified Allocation Plan | *This tool calculates the location-based criteria automatically*")