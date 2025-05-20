# import streamlit as st
# import pandas as pd
# import geopandas as gpd
# from streamlit_folium import st_folium
# import folium
# from pathlib import Path

# from aggregate_scoring import (
#     CommunityTransportationOptions,
#     DesirableUndesirableActivities,
#     QualityEducation,
#     StableCommunities
# )
# from map_layers.build_layers import *
# from map_layers.colours import YlGnBu_20, YlGnBu_5, status_colours


# ###############################################################################
# # === Load Data ===
# # --- CommunityTransportationOptions ---
# df_transit = pd.read_csv("data/community_transportation_options/georgia_transit_locations_with_hub.csv")
# # --- DesirableUndesirableActivities ---
# rural_gdf = gpd.read_file("data/shapefiles/USDA_Rural_Housing_by_Tract_7054655361891465054/USDA_Rural_Housing_by_Tract.shp").to_crs("EPSG:4326")
# rural_union = rural_gdf.unary_union 
# csv_desirable = pd.read_csv("data/desirable_undesirable_activities/desirable_activities_google_places_v3.csv")
# csv_usda = pd.read_csv("data/desirable_undesirable_activities/food_access_research_atlas.csv", dtype={'CensusTract': str})
# tract_shape = gpd.read_file("data/shapefiles/tl_2024_13_tract/tl_2024_13_tract.shp")
# csv_undesirable = pd.read_csv("data/desirable_undesirable_activities/undesirable_hsi_tri_cdr_rcra_frs_google_places.csv")
# # --- QualityEducation ---
# df_school = pd.read_csv("data/quality_education_areas/Option_C_Scores_Eligibility_with_BTO.csv")
# gdf_school_boundaries = [
#     gpd.read_file("data/quality_education_areas/Administrative.geojson").to_crs("EPSG:4326"),
#     gpd.read_file("data/quality_education_areas/APSBoundaries.json").to_crs("EPSG:4326"),
#     gpd.read_file("data/quality_education_areas/DKE.json").to_crs("EPSG:4326"),
#     gpd.read_file("data/quality_education_areas/DKM.json").to_crs("EPSG:4326"),
#     gpd.read_file("data/quality_education_areas/DKBHS.json").to_crs("EPSG:4326")
#     ]
# # --- StableCommunities ---
# df_indicators = pd.read_csv("data/stable_communities/stable_communities_2024_processed_v3.csv")

# #---------------------------------------------------------------
# # === Load Map Data ===
# gdf_total_score = gpd.read_file("data/maps/total_location_score/total_score_metro_atl.geojson")
# # --- CommunityTransportationOptions ---
# gdf_transportation_score = gpd.read_file("data/maps/community_transportation_options/transportation_options_score_metro_atl.geojson")
# # --- DesirableUndesirableActivities ---
# gdf_desirable_undesirable_score = gpd.read_file("data/maps/desirable_undesirable_activities/desirable_undesirable_score_metro_atl.geojson")
# # --- Housing Needs Indicators ---
# gdf_housing_needs = gpd.read_file("data/maps/housing_need_characteristics/housing_need_indicators_metro_atl.geojson").to_crs("EPSG:4326")
# # --- QualityEducation ---
# gdf_education_score = gpd.read_file("data/maps/quality_education_areas/education_score_metro_atl.geojson")
# # --- StableCommunities ---
# gdf_stable_communities_score = gpd.read_file("data/maps/stable_communities/stable_communities_score_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_environmental_index = gpd.read_file("data/maps/stable_communities/environmental_health_index_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_jobs_index = gpd.read_file("data/maps/stable_communities/jobs_proximity_index_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_income_index = gpd.read_file("data/maps/stable_communities/median_income_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_transit_index = gpd.read_file("data/maps/stable_communities/transit_access_index_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_poverty_index = gpd.read_file("data/maps/stable_communities/above_poverty_level_metro_atl.geojson").to_crs("EPSG:4326")
# # --- Applicant Locations ---
# gdf_applicants = gpd.read_file("data/maps/application_list_2022_2023_2024_metro_atl.geojson").to_crs("EPSG:4326")

import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium
import folium
from pathlib import Path

from aggregate_scoring import (
    CommunityTransportationOptions,
    DesirableUndesirableActivities,
    QualityEducation,
    StableCommunities
)
from map_layers.build_layers import *
from map_layers.colours import YlGnBu_20, YlGnBu_5, status_colours

# === Cache heavy data ===
@st.cache_data

def load_gdf(path):
    return gpd.read_file(path)

@st.cache_data

def load_csv(path, **kwargs):
    return pd.read_csv(path, **kwargs)


# === Load Data ===
df_transit = load_csv("data/community_transportation_options/georgia_transit_locations_with_hub.csv")
rural_gdf = load_gdf("data/shapefiles/usda_rural_tracts.geojson").to_crs("EPSG:4326")
csv_desirable = load_csv("data/desirable_undesirable_activities/desirable_activities_google_places_v3.csv")
csv_usda = load_csv("data/desirable_undesirable_activities/food_access_research_atlas.csv", dtype={'CensusTract': str})
tract_shape = load_gdf("data/shapefiles/tl_2024_13_tract/tl_2024_13_tract.shp")
csv_undesirable = load_csv("data/desirable_undesirable_activities/undesirable_hsi_tri_cdr_rcra_frs_google_places.csv")
df_school = load_csv("data/quality_education_areas/Option_C_Scores_Eligibility_with_BTO.csv")
gdf_school_boundaries = [
    load_gdf(f"data/quality_education_areas/{name}").to_crs("EPSG:4326")
    for name in ["Administrative.geojson", "APSBoundaries.json", "DKE.json", "DKM.json", "DKBHS.json"]
]
df_indicators = load_csv("data/stable_communities/stable_communities_2024_processed_v3.csv")

# Map Layers
gdf_total_score = load_gdf("data/maps/total_location_score/total_score_metro_atl.geojson")
gdf_transportation_score = load_gdf("data/maps/community_transportation_options/transportation_options_score_metro_atl.geojson")
gdf_desirable_undesirable_score = load_gdf("data/maps/desirable_undesirable_activities/desirable_undesirable_score_metro_atl.geojson")
gdf_housing_needs = load_gdf("data/maps/housing_need_characteristics/housing_need_indicators_metro_atl.geojson").to_crs("EPSG:4326")
gdf_education_score = load_gdf("data/maps/quality_education_areas/education_score_metro_atl.geojson")
gdf_stable_communities_score = load_gdf("data/maps/stable_communities/stable_communities_score_metro_atl.geojson").to_crs("EPSG:4326")
gdf_environmental_index = load_gdf("data/maps/stable_communities/environmental_health_index_metro_atl.geojson").to_crs("EPSG:4326")
gdf_jobs_index = load_gdf("data/maps/stable_communities/jobs_proximity_index_metro_atl.geojson").to_crs("EPSG:4326")
gdf_income_index = load_gdf("data/maps/stable_communities/median_income_metro_atl.geojson").to_crs("EPSG:4326")
gdf_transit_index = load_gdf("data/maps/stable_communities/transit_access_index_metro_atl.geojson").to_crs("EPSG:4326")
gdf_poverty_index = load_gdf("data/maps/stable_communities/above_poverty_level_metro_atl.geojson").to_crs("EPSG:4326")
gdf_applicants = load_gdf("data/maps/application_list_2022_2023_2024_metro_atl.geojson").to_crs("EPSG:4326")


st.title("LIHTC Location Scoring Tool")

# === Sidebar for Inputs ===
with st.sidebar:
    st.subheader("Enter Site Coordinates")
    lat_input = st.text_input("Latitude", placeholder="e.g. 33.856192")
    lon_input = st.text_input("Longitude", placeholder="e.g. -84.347348")

    # Track button click
    button_clicked = st.button("Calculate Scores")

    if button_clicked:
        try:
            latitude = float(lat_input)
            longitude = float(lon_input)
            valid_coords = True
        except ValueError:
            valid_coords = False

        if not valid_coords:
            st.warning("Please enter valid numeric coordinates.")
        else:
        # --- Load inputs ---
            kwargs = {
                # --- CommunityTransportationOptions ---
                "transit_df": df_transit,

                # --- DesirableUndesirableActivities ---
                "rural_gdf_unary_union": rural_gdf,
                "desirable_csv": csv_desirable, 
                "grocery_csv": csv_desirable,
                "usda_csv": csv_usda,
                "tract_shapefile": tract_shape,
                "undesirable_csv": csv_undesirable,

                # --- QualityEducation ---
                "school_df": df_school,
                "school_boundary_gdfs": gdf_school_boundaries,       
                "state_avg_by_year": {
                    "elementary": {
                        2018: 77.8,
                        2019: 79.9
                    },
                    "middle": {
                        2018: 76.2,
                        2019: 77
                    },
                    "high": {
                        2018: 75.3,
                        2019: 78.8
                    }
                },

                # --- StableCommunities ---
                "indicators_df": df_indicators,
                "tracts_shp": tract_shape,
            } 


            # --- Calculate each score ---
            ct_score = CommunityTransportationOptions(latitude, longitude, **kwargs).calculate_score()
            du_score = DesirableUndesirableActivities(latitude, longitude, **kwargs).calculate_score()
            qe_score = QualityEducation(latitude, longitude, **kwargs).calculate_score()
            sc_score = StableCommunities(latitude, longitude, **kwargs).calculate_score()

            total_score = ct_score + du_score + qe_score + sc_score

            # --- Display total score first ---
            st.markdown("---")
            st.markdown(
                f"""
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h4 style='margin: 0;'>Total Location Score:</h4>
                    <div style='background-color: black; color: white; padding: 8px 16px; border-radius: 8px; font-size: 20px;'>
                        {total_score:.2f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # --- Display breakdown by category in two columns ---
            st.markdown("#### Breakdown by Category")
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown("**Community Transportation Options Score:**")
                st.markdown("**Desirable/Undesirable Activities Score:**")
                st.markdown("**Quality Education Areas Score:**")
                st.markdown("**Stable Communities Score:**")

            with col2:
                st.markdown(f"{ct_score:.2f}")
                st.markdown(f"{du_score:.2f}")
                st.markdown(f"{qe_score:.2f}")
                st.markdown(f"{sc_score:.2f}")

# === TABS FOR MAP DISPLAY ===
tab1, tab2, tab3 = st.tabs([
    "Location Criteria Score Map",
    "Stable Communities Indicator Map",
    "Housing Needs Indicator Map"
])

with tab1:
    st.markdown("#### Map of Selected Layers")
    selected_layers = st.multiselect(
        "Choose layers to display:",
        options=[
            "Total Score", 
            "Desirable/Undesirable Activities Score", 
            "Community Transportation Score",
            "Stable Communities Score",
            "Quality Education Score", 
            "Applicant Locations"
        ],
        default=["Total Score", "Applicant Locations"]
    )

    # --- Dynamic map title ---
    if selected_layers:
        st.markdown(f"### Map of {', '.join(selected_layers)}")

    # --- Initialize map ---
    center_lat = gdf_total_score["lat"].mean()
    center_lon = gdf_total_score["lon"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=9, tiles="cartodbpositron")

    # --- Add layers dynamically ---
    if "Total Score" in selected_layers:
        layer, legend = add_lat_lon_score_layer(
            gdf_total_score,
            layer_name="Total Score",
            score_column="score",
            palette=YlGnBu_20,
            radius=4
        )
        layer.add_to(m)
        if legend:
            legend.add_to(m)
    if "Desirable/Undesirable Activities Score" in selected_layers:
        layer, legend = add_lat_lon_score_layer(
            gdf_desirable_undesirable_score,
            layer_name="Desirable/Undesirable Activities Score",
            score_column="score",
            palette=YlGnBu_20,
            radius=4
        )
        layer.add_to(m)
        if legend:
            legend.add_to(m)
    if "Community Transportation Score" in selected_layers:
        layer, legend = add_lat_lon_score_layer(
            gdf_transportation_score,
            layer_name="Community Transportation Score",
            score_column="score",
            palette=YlGnBu_5,
            radius=4
        )
        layer.add_to(m)
        if legend:
            legend.add_to(m)
    if "Stable Communities Score" in selected_layers:
        add_tract_score_layer_stable(
            m,
            gdf_stable_communities_score,
            score_column="score",
            layer_name="Stable Communities Score"
        )
    if "Quality Education Score" in selected_layers:
        layer = add_tract_score_layer(
            m,
            gdf_education_score,
            score_column="score",
            layer_name="Quality Education Score"
        )
        layer.add_to(m)
    if "Applicant Locations" in selected_layers:
        add_coloured_markers_to_map(
            folium_map=m,
            gdf=gdf_applicants,
            lat_col="lat",
            lon_col="lon",
            colour_by="status",
            layer_name="Applicant Locations",
            categorical_colours=status_colours
        )

    # --- Optional: Show user-inputted point ---
    if button_clicked and valid_coords and st.sidebar.button("Click to Show Site on Map"):
        folium.Marker([latitude, longitude], tooltip="Your Site").add_to(m)

    st_folium(m, width=900, height=600)

        # # --- Display results ---
        # score_labels = [
        #     ("Community Transportation Options Score", ct_score),
        #     ("Desirable/Undesirable Activities Score", du_score),
        #     ("Quality Education Areas Score", qe_score),
        #     ("Stable Communities Score", sc_score)
        # ]

        # for label, score in score_labels:
        #     st.write(f"**{label}:** {score:.2f}")

        # st.markdown("---")
        # st.markdown(f"<h4>Total Location Score: <span style='color: white; background-color: black; padding: 0.2em 0.5em; border-radius: 4px;'>{total_score:.2f}</span></h4>", unsafe_allow_html=True)
