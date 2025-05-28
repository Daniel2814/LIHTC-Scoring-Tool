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


## scoring_tool.py 
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

# # === Cache heavy data ===
# @st.cache_data

# def load_gdf(path):
#     return gpd.read_file(path)

# @st.cache_data

# def load_csv(path, **kwargs):
#     return pd.read_csv(path, **kwargs)


# # === Load Data ===
# df_transit = load_csv("data/community_transportation_options/georgia_transit_locations_with_hub.csv")
# rural_gdf = load_gdf("data/shapefiles/usda_rural_tracts.geojson").to_crs("EPSG:4326")
# rural_union = rural_gdf.geometry.unary_union
# csv_desirable = load_csv("data/desirable_undesirable_activities/desirable_activities_google_places_v3.csv")
# csv_usda = load_csv("data/desirable_undesirable_activities/food_access_research_atlas.csv", dtype={'CensusTract': str})
# tract_shape = load_gdf("data/shapefiles/tl_2024_13_tract/tl_2024_13_tract.shp")
# csv_undesirable = load_csv("data/desirable_undesirable_activities/undesirable_hsi_tri_cdr_rcra_frs_google_places.csv")
# df_school = load_csv("data/quality_education_areas/Option_C_Scores_Eligibility_with_BTO.csv")
# gdf_school_boundaries = [
#     load_gdf(f"data/quality_education_areas/{name}").to_crs("EPSG:4326")
#     for name in ["Administrative.geojson", "APSBoundaries.json", "DKE.json", "DKM.json", "DKBHS.json"]
# ]
# df_indicators = load_csv("data/stable_communities/stable_communities_2024_processed_v3.csv")

# # Map Layers
# gdf_total_score = load_gdf("data/maps/total_location_score/total_score_metro_atl.geojson")
# gdf_transportation_score = load_gdf("data/maps/community_transportation_options/transportation_options_score_metro_atl.geojson")
# gdf_desirable_undesirable_score = load_gdf("data/maps/desirable_undesirable_activities/desirable_undesirable_score_metro_atl.geojson")
# gdf_housing_needs = load_gdf("data/maps/housing_need_characteristics/housing_need_indicators_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_education_score = load_gdf("data/maps/quality_education_areas/education_score_metro_atl.geojson")
# gdf_stable_communities_score = load_gdf("data/maps/stable_communities/stable_communities_score_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_environmental_index = load_gdf("data/maps/stable_communities/environmental_health_index_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_jobs_index = load_gdf("data/maps/stable_communities/jobs_proximity_index_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_income_index = load_gdf("data/maps/stable_communities/median_income_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_transit_index = load_gdf("data/maps/stable_communities/transit_access_index_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_poverty_index = load_gdf("data/maps/stable_communities/above_poverty_level_metro_atl.geojson").to_crs("EPSG:4326")
# gdf_applicants = load_gdf("data/maps/application_list_2022_2023_2024_metro_atl.geojson").to_crs("EPSG:4326")



# st.title("LIHTC Location Scoring Tool")

# # === Sidebar for Inputs ===
# with st.sidebar:
#     st.subheader("Enter Site Coordinates")
#     lat_input = st.text_input("Latitude", placeholder="e.g. 33.856192")
#     lon_input = st.text_input("Longitude", placeholder="e.g. -84.347348")

#     # Track button click
#     button_clicked = st.button("Calculate Scores")

#     if button_clicked:
#         try:
#             latitude = float(lat_input)
#             longitude = float(lon_input)
#             valid_coords = True
#         except ValueError:
#             valid_coords = False

#         if not valid_coords:
#             st.warning("Please enter valid numeric coordinates.")
#         else:
#         # --- Load inputs ---
#             kwargs = {
#                 # --- CommunityTransportationOptions ---
#                 "transit_df": df_transit,

#                 # --- DesirableUndesirableActivities ---
#                 "rural_gdf_unary_union": rural_union,
#                 "desirable_csv": csv_desirable, 
#                 "grocery_csv": csv_desirable,
#                 "usda_csv": csv_usda,
#                 "tract_shapefile": tract_shape,
#                 "undesirable_csv": csv_undesirable,

#                 # --- QualityEducation ---
#                 "school_df": df_school,
#                 "school_boundary_gdfs": gdf_school_boundaries,       
#                 "state_avg_by_year": {
#                     "elementary": {
#                         2018: 77.8,
#                         2019: 79.9
#                     },
#                     "middle": {
#                         2018: 76.2,
#                         2019: 77
#                     },
#                     "high": {
#                         2018: 75.3,
#                         2019: 78.8
#                     }
#                 },

#                 # --- StableCommunities ---
#                 "indicators_df": df_indicators,
#                 "tracts_shp": tract_shape,
#             } 


#             # --- Calculate each score ---
#             ct_score = CommunityTransportationOptions(latitude, longitude, **kwargs).calculate_score()
#             du_score = DesirableUndesirableActivities(latitude, longitude, **kwargs).calculate_score()
#             qe_score = QualityEducation(latitude, longitude, **kwargs).calculate_score()
#             sc_score = StableCommunities(latitude, longitude, **kwargs).calculate_score()

#             total_score = ct_score + du_score + qe_score + sc_score

#             # --- Display total score first ---
#             st.markdown("---")
#             st.markdown(
#                 f"""
#                 <div style='display: flex; justify-content: space-between; align-items: center;'>
#                     <h4 style='margin: 0;'>Total Location Score:</h4>
#                     <div style='background-color: black; color: white; padding: 8px 16px; border-radius: 8px; font-size: 20px;'>
#                         {total_score:.2f}
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#             # --- Display breakdown by category in two columns ---
#             st.markdown("#### Breakdown by Category")
#             col1, col2 = st.columns([3, 1])

#             with col1:
#                 st.markdown("**Community Transportation Options Score:**")
#                 st.markdown("**Desirable/Undesirable Activities Score:**")
#                 st.markdown("**Quality Education Areas Score:**")
#                 st.markdown("**Stable Communities Score:**")

#             with col2:
#                 st.markdown(f"{ct_score:.2f}")
#                 st.markdown(f"{du_score:.2f}")
#                 st.markdown(f"{qe_score:.2f}")
#                 st.markdown(f"{sc_score:.2f}")

# # === TABS FOR MAP DISPLAY ===
# tab1, tab2, tab3 = st.tabs([
#     "Location Criteria Score Map",
#     "Stable Communities Indicator Map",
#     "Housing Needs Indicator Map"
# ])

# with tab1:
#     st.markdown("#### Map of Selected Layers")
#     selected_layers = st.multiselect(
#         "Choose layers to display:",
#         options=[
#             "Total Score", 
#             "Desirable/Undesirable Activities Score", 
#             "Community Transportation Score",
#             "Stable Communities Score",
#             "Quality Education Score", 
#             "Applicant Locations"
#         ],
#         default=["Total Score", "Applicant Locations"]
#     )

#     # --- Dynamic map title ---
#     if selected_layers:
#         st.markdown(f"### Map of {', '.join(selected_layers)}")

#     # --- Initialize map ---
#     center_lat = gdf_total_score["lat"].mean()
#     center_lon = gdf_total_score["lon"].mean()
#     m = folium.Map(location=[center_lat, center_lon], zoom_start=9, tiles="cartodbpositron")

#     # --- Add layers dynamically ---
#     if "Total Score" in selected_layers:
#         layer, legend = add_lat_lon_score_layer(
#             gdf_total_score,
#             layer_name="Total Score",
#             score_column="score",
#             palette=YlGnBu_20,
#             radius=4
#         )
#         layer.add_to(m)
#         if legend:
#             legend.add_to(m)
#     if "Desirable/Undesirable Activities Score" in selected_layers:
#         layer, legend = add_lat_lon_score_layer(
#             gdf_desirable_undesirable_score,
#             layer_name="Desirable/Undesirable Activities Score",
#             score_column="score",
#             palette=YlGnBu_20,
#             radius=4
#         )
#         layer.add_to(m)
#         if legend:
#             legend.add_to(m)
#     if "Community Transportation Score" in selected_layers:
#         layer, legend = add_lat_lon_score_layer(
#             gdf_transportation_score,
#             layer_name="Community Transportation Score",
#             score_column="score",
#             palette=YlGnBu_5,
#             radius=4
#         )
#         layer.add_to(m)
#         if legend:
#             legend.add_to(m)
#     if "Stable Communities Score" in selected_layers:
#         add_tract_score_layer_stable(
#             m,
#             gdf_stable_communities_score,
#             score_column="score",
#             layer_name="Stable Communities Score"
#         )
#     if "Quality Education Score" in selected_layers:
#         layer = add_tract_score_layer(
#             m,
#             gdf_education_score,
#             score_column="score",
#             layer_name="Quality Education Score"
#         )
#         layer.add_to(m)
#     if "Applicant Locations" in selected_layers:
#         add_coloured_markers_to_map(
#             folium_map=m,
#             gdf=gdf_applicants,
#             lat_col="lat",
#             lon_col="lon",
#             colour_by="status",
#             layer_name="Applicant Locations",
#             categorical_colours=status_colours
#         )

#     # --- Optional: Show user-inputted point ---
#     if button_clicked and valid_coords and st.sidebar.button("Click to Show Site on Map"):
#         folium.Marker([latitude, longitude], tooltip="Your Site").add_to(m)

#     st_folium(m, width=900, height=600)

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


# import streamlit as st
# import pandas as pd
# import geopandas as gpd
# from streamlit_folium import st_folium
# import folium
# from pathlib import Path
# import functools

# from aggregate_scoring import (
#     CommunityTransportationOptions,
#     DesirableUndesirableActivities,
#     QualityEducation,
#     StableCommunities
# )
# from map_layers.build_layers import *
# from map_layers.colours import YlGnBu_20, YlGnBu_5, status_colours

# # === Optimized Cache Functions ===
# @st.cache_data(ttl=3600)  # Cache for 1 hour
# def load_gdf(path):
#     """Load geodataframe with caching"""
#     return gpd.read_file(path)

# @st.cache_data(ttl=3600)
# def load_csv(path, **kwargs):
#     """Load CSV with caching"""
#     return pd.read_csv(path, **kwargs)

# # === Lazy Loading Functions ===
# @st.cache_data
# def get_core_data():
#     """Load only essential data for scoring calculations"""
#     return {
#         'df_transit': load_csv("data/community_transportation_options/georgia_transit_locations_with_hub.csv"),
#         'rural_gdf': load_gdf("data/shapefiles/usda_rural_tracts.geojson").to_crs("EPSG:4326"),
#         'csv_desirable': load_csv("data/desirable_undesirable_activities/desirable_activities_google_places_v3.csv"),
#         'csv_usda': load_csv("data/desirable_undesirable_activities/food_access_research_atlas.csv", dtype={'CensusTract': str}),
#         'tract_shape': load_gdf("data/shapefiles/tl_2024_13_tract/tl_2024_13_tract.shp"),
#         'csv_undesirable': load_csv("data/desirable_undesirable_activities/undesirable_hsi_tri_cdr_rcra_frs_google_places.csv"),
#         'df_school': load_csv("data/quality_education_areas/Option_C_Scores_Eligibility_with_BTO.csv"),
#         'df_indicators': load_csv("data/stable_communities/stable_communities_2024_processed_v3.csv")
#     }

# @st.cache_data
# def get_school_boundaries():
#     """Load school boundaries only when needed"""
#     return [
#         load_gdf(f"data/quality_education_areas/{name}").to_crs("EPSG:4326")
#         for name in ["Administrative.geojson", "APSBoundaries.json", "DKE.json", "DKM.json", "DKBHS.json"]
#     ]

# @st.cache_data
# def get_map_layer_data(layer_name):
#     """Load map layer data only when requested"""
#     layer_paths = {
#         "Total Score": "data/maps/total_location_score/total_score_metro_atl.geojson",
#         "Community Transportation Score": "data/maps/community_transportation_options/transportation_options_score_metro_atl.geojson",
#         "Desirable/Undesirable Activities Score": "data/maps/desirable_undesirable_activities/desirable_undesirable_score_metro_atl.geojson",
#         "Quality Education Score": "data/maps/quality_education_areas/education_score_metro_atl.geojson",
#         "Stable Communities Score": "data/maps/stable_communities/stable_communities_score_metro_atl.geojson",
#         "Applicant Locations": "data/maps/application_list_2022_2023_2024_metro_atl.geojson",
#         "Housing Needs": "data/maps/housing_need_characteristics/housing_need_indicators_metro_atl.geojson",
#         "Environmental Index": "data/maps/stable_communities/environmental_health_index_metro_atl.geojson",
#         "Jobs Index": "data/maps/stable_communities/jobs_proximity_index_metro_atl.geojson",
#         "Income Index": "data/maps/stable_communities/median_income_metro_atl.geojson",
#         "Transit Index": "data/maps/stable_communities/transit_access_index_metro_atl.geojson",
#         "Poverty Index": "data/maps/stable_communities/above_poverty_level_metro_atl.geojson"
#     }
    
#     if layer_name in layer_paths:
#         gdf = load_gdf(layer_paths[layer_name])
#         if gdf.crs != "EPSG:4326":
#             gdf = gdf.to_crs("EPSG:4326")
#         return gdf
#     return None

# @st.cache_data
# def get_lightweight_bounds():
#     """Get map bounds without loading full datasets"""
#     # Use a smaller representative dataset for bounds
#     sample_gdf = load_gdf("data/maps/total_location_score/total_score_metro_atl.geojson")
#     return {
#         'center_lat': sample_gdf["lat"].mean() if "lat" in sample_gdf.columns else sample_gdf.geometry.centroid.y.mean(),
#         'center_lon': sample_gdf["lon"].mean() if "lon" in sample_gdf.columns else sample_gdf.geometry.centroid.x.mean()
#     }

# def calculate_scores_if_needed(latitude, longitude):
#     """Calculate scores only when button is clicked"""
#     core_data = get_core_data()
#     school_boundaries = get_school_boundaries()
    
#     kwargs = {
#         # --- CommunityTransportationOptions ---
#         "transit_df": core_data['df_transit'],

#         # --- DesirableUndesirableActivities ---
#         "rural_gdf_unary_union": core_data['rural_gdf'].geometry.unary_union,
#         "desirable_csv": core_data['csv_desirable'], 
#         "grocery_csv": core_data['csv_desirable'],
#         "usda_csv": core_data['csv_usda'],
#         "tract_shapefile": core_data['tract_shape'],
#         "undesirable_csv": core_data['csv_undesirable'],

#         # --- QualityEducation ---
#         "school_df": core_data['df_school'],
#         "school_boundary_gdfs": school_boundaries,       
#         "state_avg_by_year": {
#             "elementary": {2018: 77.8, 2019: 79.9},
#             "middle": {2018: 76.2, 2019: 77},
#             "high": {2018: 75.3, 2019: 78.8}
#         },

#         # --- StableCommunities ---
#         "indicators_df": core_data['df_indicators'],
#         "tracts_shp": core_data['tract_shape'],
#     }

#     # Calculate scores
#     ct_score = CommunityTransportationOptions(latitude, longitude, **kwargs).calculate_score()
#     du_score = DesirableUndesirableActivities(latitude, longitude, **kwargs).calculate_score()
#     qe_score = QualityEducation(latitude, longitude, **kwargs).calculate_score()
#     sc_score = StableCommunities(latitude, longitude, **kwargs).calculate_score()

#     return ct_score, du_score, qe_score, sc_score

# # === MAIN APP ===
# st.title("LIHTC Location Scoring Tool")

# # === Sidebar for Inputs ===
# with st.sidebar:
#     st.subheader("Enter Site Coordinates")
#     lat_input = st.text_input("Latitude", placeholder="e.g. 33.856192")
#     lon_input = st.text_input("Longitude", placeholder="e.g. -84.347348")

#     # Track button click
#     button_clicked = st.button("Calculate Scores")

#     if button_clicked:
#         try:
#             latitude = float(lat_input)
#             longitude = float(lon_input)
#             valid_coords = True
#         except ValueError:
#             valid_coords = False

#         if not valid_coords:
#             st.warning("Please enter valid numeric coordinates.")
#         else:
#             # Show loading spinner
#             with st.spinner("Calculating scores..."):
#                 ct_score, du_score, qe_score, sc_score = calculate_scores_if_needed(latitude, longitude)
#                 total_score = ct_score + du_score + qe_score + sc_score

#             # Store scores in session state for map display
#             st.session_state.scores_calculated = True
#             st.session_state.latitude = latitude
#             st.session_state.longitude = longitude
#             st.session_state.ct_score = ct_score
#             st.session_state.du_score = du_score
#             st.session_state.qe_score = qe_score
#             st.session_state.sc_score = sc_score
#             st.session_state.total_score = total_score

#     # Display scores if calculated
#     if hasattr(st.session_state, 'scores_calculated') and st.session_state.scores_calculated:
#         st.markdown("---")
#         st.markdown(
#             f"""
#             <div style='display: flex; justify-content: space-between; align-items: center;'>
#                 <h4 style='margin: 0;'>Total Location Score:</h4>
#                 <div style='background-color: black; color: white; padding: 8px 16px; border-radius: 8px; font-size: 20px;'>
#                     {st.session_state.total_score:.2f}
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         # Display breakdown
#         st.markdown("#### Breakdown by Category")
#         col1, col2 = st.columns([3, 1])

#         with col1:
#             st.markdown("**Community Transportation Options Score:**")
#             st.markdown("**Desirable/Undesirable Activities Score:**")
#             st.markdown("**Quality Education Areas Score:**")
#             st.markdown("**Stable Communities Score:**")

#         with col2:
#             st.markdown(f"{st.session_state.ct_score:.2f}")
#             st.markdown(f"{st.session_state.du_score:.2f}")
#             st.markdown(f"{st.session_state.qe_score:.2f}")
#             st.markdown(f"{st.session_state.sc_score:.2f}")

# # === TABS FOR MAP DISPLAY ===
# tab1, tab2, tab3 = st.tabs([
#     "Location Criteria Score Map",
#     "Stable Communities Indicator Map",
#     "Housing Needs Indicator Map"
# ])

# with tab1:
#     st.markdown("#### Map of Selected Layers")
#     selected_layers = st.multiselect(
#         "Choose layers to display:",
#         options=[
#             "Total Score", 
#             "Desirable/Undesirable Activities Score", 
#             "Community Transportation Score",
#             "Stable Communities Score",
#             "Quality Education Score", 
#             "Applicant Locations"
#         ],
#         default=["Total Score"]  # Reduced default to single layer
#     )

#     # Only create map if layers are selected
#     if selected_layers:
#         with st.spinner("Loading map layers..."):
#             # Get map bounds efficiently
#             bounds = get_lightweight_bounds()
            
#             # Initialize map
#             m = folium.Map(
#                 location=[bounds['center_lat'], bounds['center_lon']], 
#                 zoom_start=9, 
#                 tiles="cartodbpositron"
#             )

#             # Add layers dynamically - only load what's needed
#             for layer_name in selected_layers:
#                 if layer_name == "Applicant Locations":
#                     gdf_applicants = get_map_layer_data("Applicant Locations")
#                     if gdf_applicants is not None:
#                         add_coloured_markers_to_map(
#                             folium_map=m,
#                             gdf=gdf_applicants,
#                             lat_col="lat",
#                             lon_col="lon",
#                             colour_by="status",
#                             layer_name="Applicant Locations",
#                             categorical_colours=status_colours
#                         )
#                 elif layer_name == "Total Score":
#                     gdf_total_score = get_map_layer_data("Total Score")
#                     if gdf_total_score is not None:
#                         layer, legend = add_lat_lon_score_layer(
#                             gdf_total_score,
#                             layer_name="Total Score",
#                             score_column="score",
#                             palette=YlGnBu_20,
#                             radius=4
#                         )
#                         layer.add_to(m)
#                         if legend:
#                             legend.add_to(m)
#                 elif layer_name == "Desirable/Undesirable Activities Score":
#                     gdf_layer = get_map_layer_data("Desirable/Undesirable Activities Score")
#                     if gdf_layer is not None:
#                         layer, legend = add_lat_lon_score_layer(
#                             gdf_layer,
#                             layer_name="Desirable/Undesirable Activities Score",
#                             score_column="score",
#                             palette=YlGnBu_20,
#                             radius=4
#                         )
#                         layer.add_to(m)
#                         if legend:
#                             legend.add_to(m)
#                 elif layer_name == "Community Transportation Score":
#                     gdf_layer = get_map_layer_data("Community Transportation Score")
#                     if gdf_layer is not None:
#                         layer, legend = add_lat_lon_score_layer(
#                             gdf_layer,
#                             layer_name="Community Transportation Score",
#                             score_column="score",
#                             palette=YlGnBu_5,
#                             radius=4
#                         )
#                         layer.add_to(m)
#                         if legend:
#                             legend.add_to(m)
#                 elif layer_name == "Stable Communities Score":
#                     gdf_layer = get_map_layer_data("Stable Communities Score")
#                     if gdf_layer is not None:
#                         add_tract_score_layer_stable(
#                             m,
#                             gdf_layer,
#                             score_column="score",
#                             layer_name="Stable Communities Score"
#                         )
#                 elif layer_name == "Quality Education Score":
#                     gdf_layer = get_map_layer_data("Quality Education Score")
#                     if gdf_layer is not None:
#                         layer = add_tract_score_layer(
#                             m,
#                             gdf_layer,
#                             score_column="score",
#                             layer_name="Quality Education Score"
#                         )
#                         layer.add_to(m)

#             # Add user point if coordinates are available
#             if (hasattr(st.session_state, 'scores_calculated') and 
#                 st.session_state.scores_calculated and 
#                 st.sidebar.checkbox("Show Site on Map")):
#                 folium.Marker(
#                     [st.session_state.latitude, st.session_state.longitude], 
#                     tooltip="Your Site",
#                     popup=f"Score: {st.session_state.total_score:.2f}"
#                 ).add_to(m)

#             st_folium(m, width=900, height=600)
#     else:
#         st.info("Select layers above to display the map.")

# with tab2:
#     st.markdown("#### Stable Communities Indicators")
#     stable_indicators = st.multiselect(
#         "Choose indicators to display:",
#         options=[
#             "Environmental Index",
#             "Jobs Index", 
#             "Income Index",
#             "Transit Index",
#             "Poverty Index"
#         ]
#     )
    
#     if stable_indicators:
#         with st.spinner("Loading stable communities map..."):
#             bounds = get_lightweight_bounds()
#             m2 = folium.Map(
#                 location=[bounds['center_lat'], bounds['center_lon']], 
#                 zoom_start=9, 
#                 tiles="cartodbpositron"
#             )
            
#             for indicator in stable_indicators:
#                 gdf_layer = get_map_layer_data(indicator)
#                 if gdf_layer is not None:
#                     # Add appropriate layer function based on indicator
#                     # This would need to be implemented based on your layer functions
#                     pass
            
#             st_folium(m2, width=900, height=600)
#     else:
#         st.info("Select indicators above to display the map.")

# with tab3:
#     st.markdown("#### Housing Needs Indicators")
#     if st.button("Load Housing Needs Map"):
#         with st.spinner("Loading housing needs map..."):
#             gdf_housing = get_map_layer_data("Housing Needs")
#             if gdf_housing is not None:
#                 bounds = get_lightweight_bounds()
#                 m3 = folium.Map(
#                     location=[bounds['center_lat'], bounds['center_lon']], 
#                     zoom_start=9, 
#                     tiles="cartodbpositron"
#                 )
#                 # Add housing needs layer
#                 st_folium(m3, width=900, height=600)
#             else:
#                 st.error("Housing needs data not available.")


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

# # === CUSTOM CSS FOR NARROWER SIDEBAR ===
# st.markdown("""
# <style>
#     /* Target multiple possible sidebar class names */
#     .css-1d391kg, .css-1lcbmhc, .css-1cypcdb, .css-17eq0hr, 
#     .css-1544g2n, [data-testid="stSidebar"] {
#         width: 250px !important;
#         min-width: 250px !important;
#         max-width: 250px !important;
#     }
    
#     /* Adjust main content area */
#     .main .block-container, .css-1lcbmhc, .css-1outpf7,
#     [data-testid="stMain"] {
#         margin-left: 250px !important;
#         padding-left: 1rem !important;
#     }
    
#     /* Alternative approach using data attributes */
#     section[data-testid="stSidebar"] {
#         width: 250px !important;
#     }
    
#     section[data-testid="stSidebar"] > div {
#         width: 250px !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# # === Cache heavy data ===
# @st.cache_data(persist="disk")  # Removed TTL to fix warnings
# def load_gdf(path):
#     return gpd.read_file(path)

# @st.cache_data(persist="disk")  # Removed TTL to fix warnings
# def load_csv(path, **kwargs):
#     return pd.read_csv(path, **kwargs)

# # === Lazy Loading Functions (only load when needed) ===
# @st.cache_data
# def get_core_data():
#     """Load only essential data for scoring calculations"""
#     return {
#         'df_transit': load_csv("data/community_transportation_options/georgia_transit_locations_with_hub.csv"),
#         'rural_gdf': load_gdf("data/shapefiles/usda_rural_tracts.geojson").to_crs("EPSG:4326"),
#         'csv_desirable': load_csv("data/desirable_undesirable_activities/desirable_activities_google_places_v3.csv"),
#         'csv_usda': load_csv("data/desirable_undesirable_activities/food_access_research_atlas.csv", dtype={'CensusTract': str}),
#         'tract_shape': load_gdf("data/shapefiles/tl_2024_13_tract/tl_2024_13_tract.shp"),
#         'csv_undesirable': load_csv("data/desirable_undesirable_activities/undesirable_hsi_tri_cdr_rcra_frs_google_places.csv"),
#         'df_school': load_csv("data/quality_education_areas/Option_C_Scores_Eligibility_with_BTO.csv"),
#         'df_indicators': load_csv("data/stable_communities/stable_communities_2024_processed_v3.csv")
#     }

# @st.cache_data
# def get_school_boundaries():
#     """Load school boundaries only when needed"""
#     return [
#         load_gdf(f"data/quality_education_areas/{name}").to_crs("EPSG:4326")
#         for name in ["Administrative.geojson", "APSBoundaries.json", "DKE.json", "DKM.json", "DKBHS.json"]
#     ]

# @st.cache_data
# def get_map_layer_data(layer_name):
#     """Load map layer data only when requested"""
#     layer_paths = {
#         "Total Score": "data/maps/total_location_score/total_score_metro_atl.geojson",
#         "Community Transportation Score": "data/maps/community_transportation_options/transportation_options_score_metro_atl.geojson",
#         "Desirable/Undesirable Activities Score": "data/maps/desirable_undesirable_activities/desirable_undesirable_score_metro_atl.geojson",
#         "Quality Education Score": "data/maps/quality_education_areas/education_score_metro_atl.geojson",
#         "Stable Communities Score": "data/maps/stable_communities/stable_communities_score_metro_atl.geojson",
#         "Applicant Locations": "data/maps/application_list_2022_2023_2024_metro_atl.geojson",
#         "Housing Needs": "data/maps/housing_need_characteristics/housing_need_indicators_metro_atl.geojson",
#         "Environmental Index": "data/maps/stable_communities/environmental_health_index_metro_atl.geojson",
#         "Jobs Index": "data/maps/stable_communities/jobs_proximity_index_metro_atl.geojson",
#         "Income Index": "data/maps/stable_communities/median_income_metro_atl.geojson",
#         "Transit Index": "data/maps/stable_communities/transit_access_index_metro_atl.geojson",
#         "Poverty Index": "data/maps/stable_communities/above_poverty_level_metro_atl.geojson"
#     }
    
#     if layer_name in layer_paths:
#         gdf = load_gdf(layer_paths[layer_name])
#         if gdf.crs != "EPSG:4326":
#             gdf = gdf.to_crs("EPSG:4326")
#         return gdf
#     return None

# def calculate_scores_if_needed(latitude, longitude):
#     """Calculate scores only when button is clicked"""
#     core_data = get_core_data()
#     school_boundaries = get_school_boundaries()
    
#     kwargs = {
#         # --- CommunityTransportationOptions ---
#         "transit_df": core_data['df_transit'],

#         # --- DesirableUndesirableActivities ---
#         "rural_gdf_unary_union": core_data['rural_gdf'].geometry.union_all(),  # Fixed deprecation warning
#         "desirable_csv": core_data['csv_desirable'], 
#         "grocery_csv": core_data['csv_desirable'],
#         "usda_csv": core_data['csv_usda'],
#         "tract_shapefile": core_data['tract_shape'],
#         "undesirable_csv": core_data['csv_undesirable'],

#         # --- QualityEducation ---
#         "school_df": core_data['df_school'],
#         "school_boundary_gdfs": school_boundaries,       
#         "state_avg_by_year": {
#             "elementary": {2018: 77.8, 2019: 79.9},
#             "middle": {2018: 76.2, 2019: 77},
#             "high": {2018: 75.3, 2019: 78.8}
#         },

#         # --- StableCommunities ---
#         "indicators_df": core_data['df_indicators'],
#         "tracts_shp": core_data['tract_shape'],
#     }

#     # Calculate scores
#     ct_score = CommunityTransportationOptions(latitude, longitude, **kwargs).calculate_score()
#     du_score = DesirableUndesirableActivities(latitude, longitude, **kwargs).calculate_score()
#     qe_score = QualityEducation(latitude, longitude, **kwargs).calculate_score()
#     sc_score = StableCommunities(latitude, longitude, **kwargs).calculate_score()

#     return ct_score, du_score, qe_score, sc_score

# # === MAIN APP ===
# st.title("LIHTC Location Scoring Tool")

# # Initialize session state for map stability (ONLY ONCE)
# if 'map_cache' not in st.session_state:
#     st.session_state.map_cache = {}
# if 'last_layer_selection' not in st.session_state:
#     st.session_state.last_layer_selection = []

# # === Sidebar for Inputs ===
# with st.sidebar:
#     st.subheader("Enter Site Coordinates")
    
#     # USE FORM TO PREVENT ANY RERUNS - NO ENTER PROCESSING
#     with st.form("coordinate_form", clear_on_submit=False):
#         lat_input = st.text_input(
#             "Latitude", 
#             placeholder="e.g. 33.856192",
#             help="Enter latitude and click 'Calculate Scores' button"
#         )
#         lon_input = st.text_input(
#             "Longitude", 
#             placeholder="e.g. -84.347348",
#             help="Enter longitude and click 'Calculate Scores' button"
#         )
        
#         # Customize button appearance
#         button_clicked = st.form_submit_button(
#             "Calculate Scores",
#             use_container_width=True,
#             type="primary"
#         )

#     if button_clicked:
#         # Add debug info
#         print(f"Button clicked - Current cache keys: {list(st.session_state.map_cache.keys())}")
        
#         # Check if both fields are filled
#         if not lat_input.strip() or not lon_input.strip():
#             st.warning("Enter both latitude and longitude, then click the button above")
#         else:
#             # Both fields have content, now check if they're numeric
#             try:
#                 latitude = float(lat_input)
#                 longitude = float(lon_input)
#                 valid_coords = True
#             except ValueError:
#                 valid_coords = False

#             if not valid_coords:
#                 st.warning("Please enter valid numeric coordinates.")
#             else:  # ← This should be "else:", not just "else"
#                 # Show loading spinner
#                 with st.spinner("Calculating scores..."):
#                     ct_score, du_score, qe_score, sc_score = calculate_scores_if_needed(latitude, longitude)
#                     total_score = ct_score + du_score + qe_score + sc_score

#                 # Store scores in session state for map display
#                 st.session_state.scores_calculated = True
#                 st.session_state.latitude = latitude
#                 st.session_state.longitude = longitude
#                 st.session_state.ct_score = ct_score
#                 st.session_state.du_score = du_score
#                 st.session_state.qe_score = qe_score
#                 st.session_state.sc_score = sc_score
#                 st.session_state.total_score = total_score
                
#                 # Debug: Check cache after scoring
#                 print(f"After scoring - Cache keys: {list(st.session_state.map_cache.keys())}")
            
#             # Force a gentle rerun to update display without losing cache
#             # st.rerun()

#     # Display scores if calculated
#     if hasattr(st.session_state, 'scores_calculated') and st.session_state.scores_calculated:
#         st.markdown("---")
#         st.markdown(
#             f"""
#             <div style='display: flex; justify-content: space-between; align-items: center;'>
#                 <h4 style='margin: 0;'>Total Location Score:</h4>
#                 <div style='background-color: black; color: white; padding: 8px 16px; border-radius: 8px; font-size: 20px;'>
#                     {st.session_state.total_score:.2f}
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         # Display breakdown with better alignment
#         st.markdown("#### Breakdown by Category")
        
#         # Use individual rows for better alignment when text wraps
#         score_data = [
#             ("Community Transportation Options Score:", st.session_state.ct_score),
#             ("Desirable/Undesirable Activities Score:", st.session_state.du_score),
#             ("Quality Education Areas Score:", st.session_state.qe_score),
#             ("Stable Communities Score:", st.session_state.sc_score)
#         ]
        
#         for label, score in score_data:
#             col1, col2 = st.columns([4, 1])
#             with col1:
#                 st.markdown(f"**{label}**")
#             with col2:
#                 st.markdown(f"**{score:.2f}**")

# # === TABS FOR MAP DISPLAY ===
# tab1, tab2, tab3 = st.tabs([
#     "Location Criteria Score Map",
#     "Stable Communities Indicator Map",
#     "Housing Needs Indicator Map"
# ])

# with tab1:
#     st.markdown("#### Map of Selected Layers")
#     selected_layers = st.multiselect(
#         "Choose layers to display:",
#         options=[
#             "Total Score", 
#             "Desirable/Undesirable Activities Score", 
#             "Community Transportation Score",
#             "Stable Communities Score",
#             "Quality Education Score", 
#             "Applicant Locations"
#         ],
#         default=["Total Score"],
#         key="layer_selection"
#     )

#     # Control for lat/lon score layers sampling
#     if any("Score" in layer and layer != "Applicant Locations" for layer in selected_layers):
#         max_points = st.slider(
#             "Max points for score layers (for performance tuning)",
#             min_value=2000,
#             max_value=13000,
#             value=7000,
#             step=500,
#             help="Controls how many points are shown for lat/lon score layers. Higher = more detail, lower = better performance."
#         )
#     else:
#         max_points = 7000  

#     # Map controls
#     show_user_point = st.checkbox(
#         "Show Site on Map", 
#         value=False,
#         disabled=not (hasattr(st.session_state, 'scores_calculated') and st.session_state.scores_calculated)
#     )

#     # Only render map if layers are selected
#     if selected_layers:
#         # Check if layer selection changed
#         layers_changed = selected_layers != st.session_state.last_layer_selection
        
#         # Create cache key for map stability
#         cache_key = f"{'-'.join(sorted(selected_layers))}_{max_points}"
        
#         # Debug: Print cache status
#         print(f"Map rendering - Cache key: {cache_key}")
#         print(f"Cache exists: {cache_key in st.session_state.map_cache}")
#         print(f"Layers changed: {layers_changed}")
        
#         # FIXED: Only rebuild when layers or max_points actually change
#         if layers_changed or cache_key not in st.session_state.map_cache:
#             with st.spinner("Loading map layers..."):
#                 try:
#                     # Initialize map
#                     center_lat = 33.886297
#                     center_lon = -84.362697
#                     m = folium.Map(
#                         location=[center_lat, center_lon], 
#                         zoom_start=9, 
#                         tiles="cartodbpositron",
#                         prefer_canvas=True
#                     )

#                     # Add layers dynamically - only load what's needed
#                     for layer_name in selected_layers:
#                         gdf = get_map_layer_data(layer_name)
#                         if gdf is None or gdf.empty:
#                             continue
                            
#                         if layer_name == "Applicant Locations":
#                             add_coloured_markers_to_map(
#                                 folium_map=m,
#                                 gdf=gdf,
#                                 lat_col="lat",
#                                 lon_col="lon",
#                                 colour_by="status",
#                                 layer_name="Applicant Locations",
#                                 clustered=False,  
#                                 categorical_colours=status_colours
#                             )
#                         elif layer_name == "Total Score":
#                             layer, legend = add_lat_lon_score_layer(
#                                 gdf,
#                                 layer_name="Total Score",
#                                 score_column="score",
#                                 palette=YlGnBu_20,
#                                 radius=4,
#                                 max_points=max_points  
#                             )
#                             layer.add_to(m)
#                             if legend:
#                                 legend.add_to(m)
#                         elif layer_name == "Desirable/Undesirable Activities Score":
#                             layer, legend = add_lat_lon_score_layer(
#                                 gdf,
#                                 layer_name="Desirable/Undesirable Activities Score",
#                                 score_column="score",
#                                 palette=YlGnBu_20,
#                                 radius=4,
#                                 max_points=max_points  
#                             )
#                             layer.add_to(m)
#                             if legend:
#                                 legend.add_to(m)
#                         elif layer_name == "Community Transportation Score":
#                             layer, legend = add_lat_lon_score_layer(
#                                 gdf,
#                                 layer_name="Community Transportation Score",
#                                 score_column="score",
#                                 palette=YlGnBu_5,
#                                 radius=4,
#                                 max_points=max_points
#                             )
#                             layer.add_to(m)
#                             if legend:
#                                 legend.add_to(m)
#                         elif layer_name == "Stable Communities Score":
#                             add_tract_score_layer_stable(
#                                 m,
#                                 gdf,
#                                 score_column="score",
#                                 layer_name="Stable Communities Score",
#                                 simplify_tolerance=0.005
#                             )
#                         elif layer_name == "Quality Education Score":
#                             layer = add_tract_score_layer(
#                                 m,
#                                 gdf,
#                                 score_column="score",
#                                 layer_name="Quality Education Score",
#                                 simplify_tolerance=0.005
#                             )
#                             if layer:
#                                 layer.add_to(m)

#                     # Cache the map
#                     st.session_state.map_cache[cache_key] = m
#                     st.session_state.last_layer_selection = selected_layers.copy()
                    
#                 except Exception as e:
#                     st.error(f"Error creating map: {str(e)}")
#                     st.stop()

#         # Get the cached map safely
#         if cache_key in st.session_state.map_cache:
#             cached_map = st.session_state.map_cache[cache_key]
#         else:
#             # If cache is missing, recreate it
#             st.warning("Map cache was cleared. Recreating map...")
#             st.rerun()
        
#         # Add user point if requested (without caching this change)
#         if (show_user_point and 
#             hasattr(st.session_state, 'scores_calculated') and 
#             st.session_state.scores_calculated):
#             # Create a copy of the cached map to add the user point
#             import copy
#             display_map = copy.deepcopy(cached_map)
#             folium.Marker(
#                 [st.session_state.latitude, st.session_state.longitude], 
#                 tooltip="Your Site",
#                 popup=f"Total Score: {st.session_state.total_score:.2f}",
#                 icon=folium.Icon(color='red', icon='star')
#             ).add_to(display_map)
#         else:
#             display_map = cached_map

#         # Display the map - CRITICAL: no returned objects to prevent grey-out
#         stable_key = f"main_map_{hash(tuple(sorted(selected_layers)))}"
        
#         map_data = st_folium(
#             display_map, 
#             width=700, 
#             height=600,
#             returned_objects=[],  # CRITICAL: prevents grey-out on zoom/pan
#             key=stable_key
#         )
#     else:
#         st.info("Select layers above to display the map.")

# with tab2:
#     st.markdown("#### Stable Communities Indicators")
#     st.info("Select indicators and click 'Load Map' to display stable communities data.")

# with tab3:
#     st.markdown("#### Housing Needs Indicator Map") 
#     st.info("Click 'Load Map' to display housing needs data.")


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

# # === CUSTOM CSS FOR NARROWER SIDEBAR ===
# st.markdown("""
# <style>
#     /* Target multiple possible sidebar class names */
#     .css-1d391kg, .css-1lcbmhc, .css-1cypcdb, .css-17eq0hr, 
#     .css-1544g2n, [data-testid="stSidebar"] {
#         width: 400px !important;
#         min-width: 400px !important;
#         max-width: 400px !important;
#     }
    
#     /* Adjust main content area */
#     .main .block-container, .css-1lcbmhc, .css-1outpf7,
#     [data-testid="stMain"] {
#         margin-left: 10px !important;
#         padding-left: 0rem !important;
#     }
    
# </style>
# """, unsafe_allow_html=True)

# # === Cache heavy data ===
# @st.cache_data(ttl=3600, persist="disk")
# def load_gdf(path):
#     return gpd.read_file(path)

# @st.cache_data(ttl=3600, persist="disk")
# def load_csv(path, **kwargs):
#     return pd.read_csv(path, **kwargs)

# # === Lazy Loading Functions (only load when needed) ===
# @st.cache_data
# def get_core_data():
#     """Load only essential data for scoring calculations"""
#     return {
#         'df_transit': load_csv("data/community_transportation_options/georgia_transit_locations_with_hub.csv"),
#         'rural_gdf': load_gdf("data/shapefiles/usda_rural_tracts.geojson").to_crs("EPSG:4326"),
#         'csv_desirable': load_csv("data/desirable_undesirable_activities/desirable_activities_google_places_v3.csv"),
#         'csv_usda': load_csv("data/desirable_undesirable_activities/food_access_research_atlas.csv", dtype={'CensusTract': str}),
#         'tract_shape': load_gdf("data/shapefiles/tl_2024_13_tract/tl_2024_13_tract.shp"),
#         'csv_undesirable': load_csv("data/desirable_undesirable_activities/undesirable_hsi_tri_cdr_rcra_frs_google_places.csv"),
#         'df_school': load_csv("data/quality_education_areas/Option_C_Scores_Eligibility_with_BTO.csv"),
#         'df_indicators': load_csv("data/stable_communities/stable_communities_2024_processed_v3.csv")
#     }

# @st.cache_data
# def get_school_boundaries():
#     """Load school boundaries only when needed"""
#     return [
#         load_gdf(f"data/quality_education_areas/{name}").to_crs("EPSG:4326")
#         for name in ["Administrative.geojson", "APSBoundaries.json", "DKE.json", "DKM.json", "DKBHS.json"]
#     ]

# @st.cache_data
# def get_map_layer_data(layer_name):
#     """Load map layer data only when requested"""
#     layer_paths = {
#         "Total Score": "data/maps/total_location_score/total_score_metro_atl.geojson",
#         "Community Transportation Score": "data/maps/community_transportation_options/transportation_options_score_metro_atl.geojson",
#         "Desirable/Undesirable Activities Score": "data/maps/desirable_undesirable_activities/desirable_undesirable_score_metro_atl.geojson",
#         "Quality Education Score": "data/maps/quality_education_areas/education_score_metro_atl.geojson",
#         "Stable Communities Score": "data/maps/stable_communities/stable_communities_score_metro_atl.geojson",
#         "Applicant Locations": "data/maps/application_list_2022_2023_2024_metro_atl.geojson",
#         "Housing Needs": "data/maps/housing_need_characteristics/housing_need_indicators_metro_atl.geojson",
#         "Environmental Index": "data/maps/stable_communities/environmental_health_index_metro_atl.geojson",
#         "Jobs Index": "data/maps/stable_communities/jobs_proximity_index_metro_atl.geojson",
#         "Income Index": "data/maps/stable_communities/median_income_metro_atl.geojson",
#         "Transit Index": "data/maps/stable_communities/transit_access_index_metro_atl.geojson",
#         "Poverty Index": "data/maps/stable_communities/above_poverty_level_metro_atl.geojson"
#     }
    
#     if layer_name in layer_paths:
#         gdf = load_gdf(layer_paths[layer_name])
#         if gdf.crs != "EPSG:4326":
#             gdf = gdf.to_crs("EPSG:4326")
#         return gdf
#     return None

# def calculate_scores_if_needed(latitude, longitude):
#     """Calculate scores only when button is clicked"""
#     core_data = get_core_data()
#     school_boundaries = get_school_boundaries()
    
#     kwargs = {
#         # --- CommunityTransportationOptions ---
#         "transit_df": core_data['df_transit'],

#         # --- DesirableUndesirableActivities ---
#         "rural_gdf_unary_union": core_data['rural_gdf'].geometry.unary_union,
#         "desirable_csv": core_data['csv_desirable'], 
#         "grocery_csv": core_data['csv_desirable'],
#         "usda_csv": core_data['csv_usda'],
#         "tract_shapefile": core_data['tract_shape'],
#         "undesirable_csv": core_data['csv_undesirable'],

#         # --- QualityEducation ---
#         "school_df": core_data['df_school'],
#         "school_boundary_gdfs": school_boundaries,       
#         "state_avg_by_year": {
#             "elementary": {2018: 77.8, 2019: 79.9},
#             "middle": {2018: 76.2, 2019: 77},
#             "high": {2018: 75.3, 2019: 78.8}
#         },

#         # --- StableCommunities ---
#         "indicators_df": core_data['df_indicators'],
#         "tracts_shp": core_data['tract_shape'],
#     }

#     # Calculate scores
#     ct_score = CommunityTransportationOptions(latitude, longitude, **kwargs).calculate_score()
#     du_score = DesirableUndesirableActivities(latitude, longitude, **kwargs).calculate_score()
#     qe_score = QualityEducation(latitude, longitude, **kwargs).calculate_score()
#     sc_score = StableCommunities(latitude, longitude, **kwargs).calculate_score()

#     return ct_score, du_score, qe_score, sc_score

# # === MAIN APP ===
# st.title("LIHTC Location Scoring Tool")

# # Initialize session state for map stability (ONLY ONCE)
# if 'map_cache' not in st.session_state:
#     st.session_state.map_cache = {}
# if 'last_layer_selection' not in st.session_state:
#     st.session_state.last_layer_selection = []

# # === Sidebar for Inputs ===
# with st.sidebar:
#     st.subheader("Enter Site Coordinates")
    
#     # USE FORM TO PREVENT RERUNS ON TYPING
#     with st.form("coordinate_form"):
#         lat_input = st.text_input("Latitude", placeholder="e.g. 33.856192")
#         lon_input = st.text_input("Longitude", placeholder="e.g. -84.347348")
#         button_clicked = st.form_submit_button("Calculate Scores")

#     if button_clicked:
#         try:
#             latitude = float(lat_input)
#             longitude = float(lon_input)
#             valid_coords = True
#         except ValueError:
#             valid_coords = False

#         if not valid_coords:
#             st.warning("Please enter valid numeric coordinates.")
#         else:
#             # Show loading spinner
#             with st.spinner("Calculating scores..."):
#                 ct_score, du_score, qe_score, sc_score = calculate_scores_if_needed(latitude, longitude)
#                 total_score = ct_score + du_score + qe_score + sc_score

#             # Store scores in session state for map display
#             st.session_state.scores_calculated = True
#             st.session_state.latitude = latitude
#             st.session_state.longitude = longitude
#             st.session_state.ct_score = ct_score
#             st.session_state.du_score = du_score
#             st.session_state.qe_score = qe_score
#             st.session_state.sc_score = sc_score
#             st.session_state.total_score = total_score

#     # Display scores if calculated
#     if hasattr(st.session_state, 'scores_calculated') and st.session_state.scores_calculated:
#         st.markdown("---")
#         st.markdown(
#             f"""
#             <div style='display: flex; justify-content: space-between; align-items: center;'>
#                 <h4 style='margin: 0;'>Total Location Score:</h4>
#                 <div style='background-color: black; color: white; padding: 8px 16px; border-radius: 8px; font-size: 20px;'>
#                     {st.session_state.total_score:.2f}
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         # Display breakdown
#         st.markdown("#### Breakdown by Category")
#         col1, col2 = st.columns([3, 1])

#         with col1:
#             st.markdown("**Community Transportation Options Score:**")
#             st.markdown("**Desirable/Undesirable Activities Score:**")
#             st.markdown("**Quality Education Areas Score:**")
#             st.markdown("**Stable Communities Score:**")

#         with col2:
#             st.markdown(f"{st.session_state.ct_score:.2f}")
#             st.markdown(f"{st.session_state.du_score:.2f}")
#             st.markdown(f"{st.session_state.qe_score:.2f}")
#             st.markdown(f"{st.session_state.sc_score:.2f}")

# # === TABS FOR MAP DISPLAY ===
# tab1, tab2, tab3 = st.tabs([
#     "Location Criteria Score Map",
#     "Stable Communities Indicator Map",
#     "Housing Needs Indicator Map"
# ])

# with tab1:
#     st.markdown("#### Map of Selected Layers")
#     selected_layers = st.multiselect(
#         "Choose layers to display:",
#         options=[
#             "Total Score", 
#             "Desirable/Undesirable Activities Score", 
#             "Community Transportation Score",
#             "Stable Communities Score",
#             "Quality Education Score", 
#             "Applicant Locations"
#         ],
#         default=["Total Score"],
#         key="layer_selection"
#     )

#     # Control for lat/lon score layers sampling
#     if any("Score" in layer and layer != "Applicant Locations" for layer in selected_layers):
#         max_points = st.slider(
#             "Max points for score layers (for performance tuning)",
#             min_value=2000,
#             max_value=13000,
#             value=7000,
#             step=500,
#             help="Controls how many points are shown for lat/lon score layers. Higher = more detail, lower = better performance."
#         )
#     else:
#         max_points = 7000  

#     # Map controls
#     show_user_point = st.checkbox(
#         "Show Site on Map", 
#         value=False,
#         disabled=not (hasattr(st.session_state, 'scores_calculated') and st.session_state.scores_calculated)
#     )

#     # Only render map if layers are selected
#     if selected_layers:
#         # Check if layer selection changed
#         layers_changed = selected_layers != st.session_state.last_layer_selection
        
#         # Create cache key for map stability
#         cache_key = f"{'-'.join(sorted(selected_layers))}_{max_points}"
        
#         # FIXED: Rebuild map when needed (removed problematic condition)
#         if layers_changed or cache_key not in st.session_state.map_cache:
#             with st.spinner("Loading map layers..."):
#                 try:
#                     # Initialize map
#                     center_lat = 33.886297
#                     center_lon = -84.362697
#                     m = folium.Map(
#                         location=[center_lat, center_lon], 
#                         zoom_start=9, 
#                         tiles="cartodbpositron",
#                         prefer_canvas=True
#                     )

#                     # Add layers dynamically - only load what's needed
#                     for layer_name in selected_layers:
#                         gdf = get_map_layer_data(layer_name)
#                         if gdf is None or gdf.empty:
#                             continue
                            
#                         if layer_name == "Applicant Locations":
#                             add_coloured_markers_to_map(
#                                 folium_map=m,
#                                 gdf=gdf,
#                                 lat_col="lat",
#                                 lon_col="lon",
#                                 colour_by="status",
#                                 layer_name="Applicant Locations",
#                                 clustered=False,  
#                                 categorical_colours=status_colours
#                             )
#                         elif layer_name == "Total Score":
#                             layer, legend = add_lat_lon_score_layer(
#                                 gdf,
#                                 layer_name="Total Score",
#                                 score_column="score",
#                                 palette=YlGnBu_20,
#                                 radius=4,
#                                 max_points=max_points  
#                             )
#                             layer.add_to(m)
#                             if legend:
#                                 legend.add_to(m)
#                         elif layer_name == "Desirable/Undesirable Activities Score":
#                             layer, legend = add_lat_lon_score_layer(
#                                 gdf,
#                                 layer_name="Desirable/Undesirable Activities Score",
#                                 score_column="score",
#                                 palette=YlGnBu_20,
#                                 radius=4,
#                                 max_points=max_points  
#                             )
#                             layer.add_to(m)
#                             if legend:
#                                 legend.add_to(m)
#                         elif layer_name == "Community Transportation Score":
#                             layer, legend = add_lat_lon_score_layer(
#                                 gdf,
#                                 layer_name="Community Transportation Score",
#                                 score_column="score",
#                                 palette=YlGnBu_5,
#                                 radius=4,
#                                 max_points=max_points
#                             )
#                             layer.add_to(m)
#                             if legend:
#                                 legend.add_to(m)
#                         elif layer_name == "Stable Communities Score":
#                             add_tract_score_layer_stable(
#                                 m,
#                                 gdf,
#                                 score_column="score",
#                                 layer_name="Stable Communities Score",
#                                 simplify_tolerance=0.005
#                             )
#                         elif layer_name == "Quality Education Score":
#                             layer = add_tract_score_layer(
#                                 m,
#                                 gdf,
#                                 score_column="score",
#                                 layer_name="Quality Education Score",
#                                 simplify_tolerance=0.005
#                             )
#                             if layer:
#                                 layer.add_to(m)

#                     # Cache the map
#                     st.session_state.map_cache[cache_key] = m
#                     st.session_state.last_layer_selection = selected_layers.copy()
                    
#                 except Exception as e:
#                     st.error(f"Error creating map: {str(e)}")
#                     st.stop()

#         # Get the cached map
#         cached_map = st.session_state.map_cache[cache_key]
        
#         # Add user point if requested (without caching this change)
#         if (show_user_point and 
#             hasattr(st.session_state, 'scores_calculated') and 
#             st.session_state.scores_calculated):
#             # Create a copy of the cached map to add the user point
#             import copy
#             display_map = copy.deepcopy(cached_map)
#             folium.Marker(
#                 [st.session_state.latitude, st.session_state.longitude], 
#                 tooltip="Your Site",
#                 popup=f"Total Score: {st.session_state.total_score:.2f}",
#                 icon=folium.Icon(color='red', icon='star')
#             ).add_to(display_map)
#         else:
#             display_map = cached_map

#         # Display the map - CRITICAL: no returned objects to prevent grey-out
#         stable_key = f"main_map_{hash(tuple(sorted(selected_layers)))}"
        
#         map_data = st_folium(
#             display_map, 
#             width=700, 
#             height=600,
#             returned_objects=[],  # CRITICAL: prevents grey-out on zoom/pan
#             key=stable_key
#         )
#     else:
#         st.info("Select layers above to display the map.")

# with tab2:
#     st.markdown("#### Stable Communities Indicators")
#     st.info("Select indicators and click 'Load Map' to display stable communities data.")

# with tab3:
#     st.markdown("#### Housing Needs Indicator Map") 
#     st.info("Click 'Load Map' to display housing needs data.")


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


# # === Cache heavy data ===
# @st.cache_data(persist="disk")  # Removed TTL to fix warnings
# def load_gdf(path):
#     return gpd.read_file(path)

# @st.cache_data(persist="disk")  # Removed TTL to fix warnings
# def load_csv(path, **kwargs):
#     return pd.read_csv(path, **kwargs)

# # === Lazy Loading Functions (only load when needed) ===
# @st.cache_data
# def get_core_data():
#     """Load only essential data for scoring calculations"""
#     return {
#         'df_transit': load_csv("data/community_transportation_options/georgia_transit_locations_with_hub.csv"),
#         'rural_gdf': load_gdf("data/shapefiles/usda_rural_tracts.geojson").to_crs("EPSG:4326"),
#         'csv_desirable': load_csv("data/desirable_undesirable_activities/desirable_activities_google_places_v3.csv"),
#         'csv_usda': load_csv("data/desirable_undesirable_activities/food_access_research_atlas.csv", dtype={'CensusTract': str}),
#         'tract_shape': load_gdf("data/shapefiles/tl_2024_13_tract/tl_2024_13_tract.shp"),
#         'csv_undesirable': load_csv("data/desirable_undesirable_activities/undesirable_hsi_tri_cdr_rcra_frs_google_places.csv"),
#         'df_school': load_csv("data/quality_education_areas/Option_C_Scores_Eligibility_with_BTO.csv"),
#         'df_indicators': load_csv("data/stable_communities/stable_communities_2024_processed_v3.csv")
#     }

# @st.cache_data
# def get_school_boundaries():
#     """Load school boundaries only when needed"""
#     return [
#         load_gdf(f"data/quality_education_areas/{name}").to_crs("EPSG:4326")
#         for name in ["Administrative.geojson", "APSBoundaries.json", "DKE.json", "DKM.json", "DKBHS.json"]
#     ]

# @st.cache_data
# def get_map_layer_data(layer_name):
#     """Load map layer data only when requested"""
#     layer_paths = {
#         "Total Score": "data/maps/total_location_score/total_score_metro_atl.geojson",
#         "Community Transportation Score": "data/maps/community_transportation_options/transportation_options_score_metro_atl.geojson",
#         "Desirable/Undesirable Activities Score": "data/maps/desirable_undesirable_activities/desirable_undesirable_score_metro_atl.geojson",
#         "Quality Education Score": "data/maps/quality_education_areas/education_score_metro_atl.geojson",
#         "Stable Communities Score": "data/maps/stable_communities/stable_communities_score_metro_atl.geojson",
#         "Applicant Locations": "data/maps/application_list_2022_2023_2024_metro_atl.geojson",
#         "Housing Needs": "data/maps/housing_need_characteristics/housing_need_indicators_metro_atl.geojson",
#         "Environmental Index": "data/maps/stable_communities/environmental_health_index_metro_atl.geojson",
#         "Jobs Index": "data/maps/stable_communities/jobs_proximity_index_metro_atl.geojson",
#         "Income Index": "data/maps/stable_communities/median_income_metro_atl.geojson",
#         "Transit Index": "data/maps/stable_communities/transit_access_index_metro_atl.geojson",
#         "Poverty Index": "data/maps/stable_communities/above_poverty_level_metro_atl.geojson"
#     }
    
#     if layer_name in layer_paths:
#         gdf = load_gdf(layer_paths[layer_name])
#         if gdf.crs != "EPSG:4326":
#             gdf = gdf.to_crs("EPSG:4326")
#         return gdf
#     return None

# def calculate_scores_if_needed(latitude, longitude):
#     """Calculate scores only when button is clicked"""
#     core_data = get_core_data()
#     school_boundaries = get_school_boundaries()
    
#     kwargs = {
#         # --- CommunityTransportationOptions ---
#         "transit_df": core_data['df_transit'],

#         # --- DesirableUndesirableActivities ---
#         "rural_gdf_unary_union": core_data['rural_gdf'].geometry.union_all(),  # Fixed deprecation warning
#         "desirable_csv": core_data['csv_desirable'], 
#         "grocery_csv": core_data['csv_desirable'],
#         "usda_csv": core_data['csv_usda'],
#         "tract_shapefile": core_data['tract_shape'],
#         "undesirable_csv": core_data['csv_undesirable'],

#         # --- QualityEducation ---
#         "school_df": core_data['df_school'],
#         "school_boundary_gdfs": school_boundaries,       
#         "state_avg_by_year": {
#             "elementary": {2018: 77.8, 2019: 79.9},
#             "middle": {2018: 76.2, 2019: 77},
#             "high": {2018: 75.3, 2019: 78.8}
#         },

#         # --- StableCommunities ---
#         "indicators_df": core_data['df_indicators'],
#         "tracts_shp": core_data['tract_shape'],
#     }

#     # Calculate scores
#     ct_score = CommunityTransportationOptions(latitude, longitude, **kwargs).calculate_score()
#     du_score = DesirableUndesirableActivities(latitude, longitude, **kwargs).calculate_score()
#     qe_score = QualityEducation(latitude, longitude, **kwargs).calculate_score()
#     sc_score = StableCommunities(latitude, longitude, **kwargs).calculate_score()

#     return ct_score, du_score, qe_score, sc_score

# # === MAIN APP ===
# st.title("LIHTC Location Scoring Tool")

# # Initialize session state for map stability (ONLY ONCE)
# if 'map_cache' not in st.session_state:
#     st.session_state.map_cache = {}
# if 'last_layer_selection' not in st.session_state:
#     st.session_state.last_layer_selection = []
# if 'current_max_points' not in st.session_state:
#     st.session_state.current_max_points = 7000

# # === Sidebar for Inputs ===
# with st.sidebar:
#     st.subheader("Enter Site Coordinates")
    
#     # USE FORM TO PREVENT ANY RERUNS - NO ENTER PROCESSING
#     with st.form("coordinate_form", clear_on_submit=False):
#         lat_input = st.text_input(
#             "Latitude", 
#             placeholder="e.g. 33.856192",
#             # help="Enter latitude and click 'Calculate Scores' button"
#         )
#         lon_input = st.text_input(
#             "Longitude", 
#             placeholder="e.g. -84.347348",
#             # help="Enter longitude and click 'Calculate Scores' button"
#         )
        
#         # Customize button appearance
#         button_clicked = st.form_submit_button(
#             "Calculate Scores",
#             use_container_width=True,
#             type="primary"
#         )

#     if button_clicked:
#         # Add debug info
#         print(f"Button clicked - Current cache keys: {list(st.session_state.map_cache.keys())}")
        
#         try:
#             latitude = float(lat_input)
#             longitude = float(lon_input)
#             valid_coords = True
#         except ValueError:
#             valid_coords = False

#         if not valid_coords:
#             st.warning("Please enter valid numeric coordinates.")
#         else:
#             # Show loading spinner
#             with st.spinner("Calculating scores..."):
#                 ct_score, du_score, qe_score, sc_score = calculate_scores_if_needed(latitude, longitude)
#                 total_score = ct_score + du_score + qe_score + sc_score

#             # Store scores in session state for map display
#             st.session_state.scores_calculated = True
#             st.session_state.latitude = latitude
#             st.session_state.longitude = longitude
#             st.session_state.ct_score = ct_score
#             st.session_state.du_score = du_score
#             st.session_state.qe_score = qe_score
#             st.session_state.sc_score = sc_score
#             st.session_state.total_score = total_score
            
#             # Debug: Check cache after scoring
#             print(f"After scoring - Cache keys: {list(st.session_state.map_cache.keys())}")
            
#             # Force a gentle rerun to update display without losing cache
#             # But DON'T trigger layer change detection
#             st.session_state.prevent_layer_change_detection = True
#             st.rerun()

#     # Display scores if calculated
#     if hasattr(st.session_state, 'scores_calculated') and st.session_state.scores_calculated:
#         st.markdown("---")
#         st.markdown(
#             f"""
#             <div style='display: flex; justify-content: space-between; align-items: center;'>
#                 <h4 style='margin: 0;'>Total Location Score:</h4>
#                 <div style='background-color: black; color: white; padding: 8px 16px; border-radius: 8px; font-size: 20px;'>
#                     {st.session_state.total_score:.2f}
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         # Display breakdown with better alignment
#         st.markdown("#### Breakdown by Category")
        
#         # Use individual rows for better alignment when text wraps
#         score_data = [
#             ("Community Transportation Options Score:", st.session_state.ct_score),
#             ("Desirable/Undesirable Activities Score:", st.session_state.du_score),
#             ("Quality Education Areas Score:", st.session_state.qe_score),
#             ("Stable Communities Score:", st.session_state.sc_score)
#         ]
        
#         for label, score in score_data:
#             col1, col2 = st.columns([4, 1])
#             with col1:
#                 st.markdown(f"**{label}**")
#             with col2:
#                 st.markdown(f"**{score:.2f}**")

# # === TABS FOR MAP DISPLAY ===
# tab1, tab2, tab3 = st.tabs([
#     "Location Criteria Score Map",
#     "Stable Communities Indicator Map",
#     "Housing Needs Indicator Map"
# ])

# with tab1:
#     st.markdown("#### Map of Selected Layers")
#     selected_layers = st.multiselect(
#         "Choose layers to display:",
#         options=[
#             "Total Score", 
#             "Desirable/Undesirable Activities Score", 
#             "Community Transportation Score",
#             "Stable Communities Score",
#             "Quality Education Score", 
#             "Applicant Locations"
#         ],
#         default=["Total Score"],
#         key="layer_selection"
#     )

#     # Control for lat/lon score layers sampling
#     if any("Score" in layer and layer != "Applicant Locations" for layer in selected_layers):
#         max_points = st.slider(
#             "Max points for score layers (for performance tuning)",
#             min_value=2000,
#             max_value=13000,
#             value=7000,
#             step=500,
#             help="Controls how many points are shown for lat/lon score layers. Higher = more detail, lower = better performance."
#         )
#     else:
#         max_points = 7000  

#     # Map controls
#     show_user_point = st.checkbox(
#         "Show Site on Map", 
#         value=False,
#         disabled=not (hasattr(st.session_state, 'scores_calculated') and st.session_state.scores_calculated)
#     )

#     # Only render map if layers are selected
#     if selected_layers:
#         # FIXED: Smarter layer change detection
#         if hasattr(st.session_state, 'prevent_layer_change_detection'):
#             # This is a rerun from scoring, don't treat as layer change
#             layers_changed = False
#             del st.session_state.prevent_layer_change_detection
#         else:
#             # Normal layer change detection
#             layers_changed = selected_layers != st.session_state.last_layer_selection
        
#         # Also check if max_points changed
#         max_points_changed = max_points != st.session_state.current_max_points
        
#         # Create cache key for map stability
#         cache_key = f"{'-'.join(sorted(selected_layers))}_{max_points}"
        
#         # Debug: Print cache status
#         print(f"Map rendering - Cache key: {cache_key}")
#         print(f"Cache exists: {cache_key in st.session_state.map_cache}")
#         print(f"Layers changed: {layers_changed}")
#         print(f"Max points changed: {max_points_changed}")
        
#         # FIXED: Only rebuild when layers or max_points actually change
#         if layers_changed or max_points_changed or cache_key not in st.session_state.map_cache:
#             with st.spinner("Loading map layers..."):
#                 try:
#                     # Initialize map
#                     center_lat = 33.886297
#                     center_lon = -84.362697
#                     m = folium.Map(
#                         location=[center_lat, center_lon], 
#                         zoom_start=9, 
#                         tiles="cartodbpositron",
#                         prefer_canvas=True
#                     )

#                     # Add layers dynamically - only load what's needed
#                     for layer_name in selected_layers:
#                         gdf = get_map_layer_data(layer_name)
#                         if gdf is None or gdf.empty:
#                             continue
                            
#                         if layer_name == "Applicant Locations":
#                             add_coloured_markers_to_map(
#                                 folium_map=m,
#                                 gdf=gdf,
#                                 lat_col="lat",
#                                 lon_col="lon",
#                                 colour_by="status",
#                                 layer_name="Applicant Locations",
#                                 clustered=False,  
#                                 categorical_colours=status_colours
#                             )
#                         elif layer_name == "Total Score":
#                             layer, legend = add_lat_lon_score_layer(
#                                 gdf,
#                                 layer_name="Total Score",
#                                 score_column="score",
#                                 palette=YlGnBu_20,
#                                 radius=4,
#                                 max_points=max_points  
#                             )
#                             layer.add_to(m)
#                             if legend:
#                                 legend.add_to(m)
#                         elif layer_name == "Desirable/Undesirable Activities Score":
#                             layer, legend = add_lat_lon_score_layer(
#                                 gdf,
#                                 layer_name="Desirable/Undesirable Activities Score",
#                                 score_column="score",
#                                 palette=YlGnBu_20,
#                                 radius=4,
#                                 max_points=max_points  
#                             )
#                             layer.add_to(m)
#                             if legend:
#                                 legend.add_to(m)
#                         elif layer_name == "Community Transportation Score":
#                             layer, legend = add_lat_lon_score_layer(
#                                 gdf,
#                                 layer_name="Community Transportation Score",
#                                 score_column="score",
#                                 palette=YlGnBu_5,
#                                 radius=4,
#                                 max_points=max_points
#                             )
#                             layer.add_to(m)
#                             if legend:
#                                 legend.add_to(m)
#                         elif layer_name == "Stable Communities Score":
#                             add_tract_score_layer_stable(
#                                 m,
#                                 gdf,
#                                 score_column="score",
#                                 layer_name="Stable Communities Score",
#                                 simplify_tolerance=0.005
#                             )
#                         elif layer_name == "Quality Education Score":
#                             layer = add_tract_score_layer(
#                                 m,
#                                 gdf,
#                                 score_column="score",
#                                 layer_name="Quality Education Score",
#                                 simplify_tolerance=0.005
#                             )
#                             if layer:
#                                 layer.add_to(m)

#                     # Cache the map
#                     st.session_state.map_cache[cache_key] = m
#                     st.session_state.last_layer_selection = selected_layers.copy()
#                     st.session_state.current_max_points = max_points
                    
#                 except Exception as e:
#                     st.error(f"Error creating map: {str(e)}")
#                     st.stop()

#         # Get the cached map safely
#         if cache_key in st.session_state.map_cache:
#             cached_map = st.session_state.map_cache[cache_key]
#         else:
#             # If cache is missing, recreate it
#             st.warning("Map cache was cleared. Recreating map...")
#             st.rerun()
        
#         # Add user point if requested (without caching this change)
#         if (show_user_point and 
#             hasattr(st.session_state, 'scores_calculated') and 
#             st.session_state.scores_calculated):
#             # Create a copy of the cached map to add the user point
#             import copy
#             display_map = copy.deepcopy(cached_map)
#             folium.Marker(
#                 [st.session_state.latitude, st.session_state.longitude], 
#                 tooltip="Your Site",
#                 popup=f"Total Score: {st.session_state.total_score:.2f}",
#                 icon=folium.Icon(color='red', icon='star')
#             ).add_to(display_map)
#         else:
#             display_map = cached_map

#         # Display the map - CRITICAL: no returned objects to prevent grey-out
#         stable_key = f"main_map_{hash(tuple(sorted(selected_layers)))}"
        
#         map_data = st_folium(
#             display_map, 
#             width=700, 
#             height=600,
#             returned_objects=[],  # CRITICAL: prevents grey-out on zoom/pan
#             key=stable_key
#         )
#     else:
#         st.info("Select layers above to display the map.")

# with tab2:
#     st.markdown("#### Stable Communities Indicators")
#     st.info("Select indicators and click 'Load Map' to display stable communities data.")

# with tab3:
#     st.markdown("#### Housing Needs Indicator Map") 
#     st.info("Click 'Load Map' to display housing needs data.")