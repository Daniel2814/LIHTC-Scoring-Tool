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

@st.cache_data(persist="disk")
def load_gdf(path):
    return gpd.read_file(path)

@st.cache_data(persist="disk")
def load_csv(path, **kwargs):
    return pd.read_csv(path, **kwargs)

@st.cache_data
def get_core_data():
    """Load only essential data for scoring calculations"""
    return {
        'df_transit': load_csv("data/community_transportation_options/georgia_transit_locations_with_hub.csv"),
        'rural_gdf': load_gdf("data/shapefiles/usda_rural_tracts.geojson").to_crs("EPSG:4326"),
        'csv_desirable': load_csv("data/desirable_undesirable_activities/desirable_activities_google_places_v3.csv"),
        'csv_usda': load_csv("data/desirable_undesirable_activities/food_access_research_atlas.csv", dtype={'CensusTract': str}),
        'tract_shape': load_gdf("data/shapefiles/tl_2024_13_tract/tl_2024_13_tract.shp"),
        'csv_undesirable': load_csv("data/desirable_undesirable_activities/undesirable_hsi_tri_cdr_rcra_frs_google_places.csv"),
        'df_school': load_csv("data/quality_education_areas/Option_C_Scores_Eligibility_with_BTO.csv"),
        'df_indicators': load_csv("data/stable_communities/stable_communities_2024_processed_v3.csv")
    }

@st.cache_data
def get_school_boundaries():
    """Load school boundaries only when needed"""
    return [
        load_gdf(f"data/quality_education_areas/{name}").to_crs("EPSG:4326")
        for name in ["Administrative.geojson", "APSBoundaries.json", "DKE.json", "DKM.json", "DKBHS.json"]
    ]

@st.cache_data
def get_map_layer_data(layer_name):
    """Load map layer data only when requested"""
    layer_paths = {
        "Total Score": "data/maps/total_location_score/total_score_metro_atl.geojson",
        "Community Transportation Score": "data/maps/community_transportation_options/transportation_options_score_metro_atl.geojson",
        "Desirable/Undesirable Activities Score": "data/maps/desirable_undesirable_activities/desirable_undesirable_score_metro_atl.geojson",
        "Quality Education Score": "data/maps/quality_education_areas/education_score_metro_atl.geojson",
        "Stable Communities Score": "data/maps/stable_communities/stable_communities_score_metro_atl.geojson",
        "Applicant Locations": "data/maps/application_list_2022_2023_2024_metro_atl.geojson",
        "Housing Needs": "data/maps/housing_need_characteristics/housing_need_indicators_metro_atl.geojson",
        "Environmental Index": "data/maps/stable_communities/environmental_health_index_metro_atl.geojson",
        "Jobs Index": "data/maps/stable_communities/jobs_proximity_index_metro_atl.geojson",
        "Income Index": "data/maps/stable_communities/median_income_metro_atl.geojson",
        "Transit Index": "data/maps/stable_communities/transit_access_index_metro_atl.geojson",
        "Poverty Index": "data/maps/stable_communities/above_poverty_level_metro_atl.geojson"
    }
    
    if layer_name in layer_paths:
        gdf = load_gdf(layer_paths[layer_name])
        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")
        return gdf
    return None

def calculate_scores_if_needed(latitude, longitude):
    """Calculate scores only when button is clicked"""
    core_data = get_core_data()
    school_boundaries = get_school_boundaries()
    
    kwargs = {
        # --- CommunityTransportationOptions ---
        "transit_df": core_data['df_transit'],

        # --- DesirableUndesirableActivities ---
        "rural_gdf_unary_union": core_data['rural_gdf'].geometry.union_all(),
        "desirable_csv": core_data['csv_desirable'], 
        "grocery_csv": core_data['csv_desirable'],
        "usda_csv": core_data['csv_usda'],
        "tract_shapefile": core_data['tract_shape'],
        "undesirable_csv": core_data['csv_undesirable'],

        # --- QualityEducation ---
        "school_df": core_data['df_school'],
        "school_boundary_gdfs": school_boundaries,       
        "state_avg_by_year": {
            "elementary": {2018: 77.8, 2019: 79.9},
            "middle": {2018: 76.2, 2019: 77},
            "high": {2018: 75.3, 2019: 78.8}
        },

        # --- StableCommunities ---
        "indicators_df": core_data['df_indicators'],
        "tracts_shp": core_data['tract_shape'],
    }

    # Calculate scores
    ct_score = CommunityTransportationOptions(latitude, longitude, **kwargs).calculate_score()
    du_score = DesirableUndesirableActivities(latitude, longitude, **kwargs).calculate_score()
    qe_score = QualityEducation(latitude, longitude, **kwargs).calculate_score()
    sc_score = StableCommunities(latitude, longitude, **kwargs).calculate_score()

    return ct_score, du_score, qe_score, sc_score

st.set_page_config(layout="wide")

# === INITIALIZE DEFAULTS ===
if "map_form_submitted" not in st.session_state:
    st.session_state.map_form_submitted = True 
    st.session_state.last_layer_selection = ["Total Score", "Applicant Locations"]
    st.session_state.last_max_points = 5000
    st.session_state.show_user_point = False


if 'lat_main' not in st.session_state:
    st.session_state.lat_main = ""

if 'lon_main' not in st.session_state:
    st.session_state.lon_main = ""

# === MAIN APP ===
st.title("LIHTC Location Scoring Tool")

# Initialize session state for map stability
if 'map_cache' not in st.session_state:
    st.session_state.map_cache = {}
if 'last_layer_selection' not in st.session_state:
    st.session_state.last_layer_selection = []


main_col1, space_column, main_col2 = st.columns([4, 1, 7])


with main_col1:
    st.subheader("Enter Site Coordinates")

    # Create a form to wrap both inputs and the button
    with st.form(key="latlon_form"):
        lat_input = st.text_input(
            "Latitude", 
            placeholder="e.g. 33.856192",
            key="lat_main"
        )

        lon_input = st.text_input(
            "Longitude", 
            placeholder="e.g. -84.347348", 
            key="lon_main"
        )

        submit_button = st.form_submit_button(
            label="Calculate Scores"
        )

    if submit_button:
        # Check if both fields are filled
        if not lat_input.strip() or not lon_input.strip():
            st.warning("Enter both latitude and longitude, then click Calculate Scores")
        else:
            try:
                latitude = float(lat_input)
                longitude = float(lon_input)
                valid_coords = True
            except ValueError:
                valid_coords = False

            if not valid_coords:
                st.warning("Please enter valid numeric coordinates.")
            else:
                with st.spinner("Calculating scores..."):
                    ct_score, du_score, qe_score, sc_score = calculate_scores_if_needed(latitude, longitude)
                    total_score = ct_score + du_score + qe_score + sc_score

                # Save to session state
                st.session_state.scores_calculated = True
                st.session_state.latitude = latitude
                st.session_state.longitude = longitude
                st.session_state.ct_score = ct_score
                st.session_state.du_score = du_score
                st.session_state.qe_score = qe_score
                st.session_state.sc_score = sc_score
                st.session_state.total_score = total_score

    # Display scores if calculated
    if hasattr(st.session_state, 'scores_calculated') and st.session_state.scores_calculated:
        st.markdown("---")
        st.markdown(
            f"""
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;'>
                <h4 style='margin: 0;'>Total Location Score:</h4>
                <div style='background-color: #1f77b4; color: white; padding: 8px 16px; border-radius: 8px; font-size: 20px; font-weight: bold;'>
                    {st.session_state.total_score:.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Display breakdown with better alignment
        st.markdown(
            "<h4 style='margin-bottom: 14px;'>Breakdown by Category</h4>",
            unsafe_allow_html=True
        )

        score_data = [
            ("Community Transport Options Score:", st.session_state.ct_score),
            ("Desirable/Undesirable Activities Score:", st.session_state.du_score),
            ("Quality Education Areas Score:", st.session_state.qe_score),
            ("Stable Communities Score:", st.session_state.sc_score)
        ]
        
        for label, score in score_data:
            col1, col2 = st.columns([5, 3])
            with col1:
                # st.markdown(f"**{label}**")
                st.markdown(
                    f"""
                    <div style='margin-bottom: 28px; font-size: 16px;'>
                        {label}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    f"""
                    <div style='text-align: right; font-weight: bold; font-size: 16px;'>
                        {score:.2f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )



with main_col2:

    # === TABS FOR MAP DISPLAY ===
    tab1, tab2, tab3 = st.tabs([
        "Location Criteria Score Map",
        "Stable Communities Indicator Map",
        "Housing Needs Indicator Map"
    ])

    with tab1:
        st.markdown("#### Map of Selected Layers")

        with st.form(key="map_layer_form"):
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
                default=st.session_state.get("last_layer_selection", ["Total Score"]),
                key="layer_selection"
            )

            if any("Score" in layer and layer != "Applicant Locations" for layer in selected_layers):
                max_points = st.slider(
                    "Max points for score layers (for performance tuning)",
                    min_value=5000,
                    max_value=13000,
                    value=st.session_state.get("last_max_points", 5000),
                    step=500,
                    key="max_points_slider"
                )
            else:
                max_points = 5000

            show_user_point = st.checkbox(
                "Show Site on Map",
                value=st.session_state.get("show_user_point", False),
                disabled=not st.session_state.get("scores_calculated", False),
                key="show_user_point_checkbox"
            )

            update_map_button = st.form_submit_button("Update Map")

        # Store updated form inputs in session state
        if update_map_button:
            st.session_state.last_layer_selection = selected_layers
            st.session_state.last_max_points = max_points
            st.session_state.show_user_point = show_user_point
            st.session_state.map_form_submitted = True

        # === MAP LOGIC ===
        cache_key = f"{'-'.join(sorted(selected_layers))}_{max_points}"
        # Verify that the cached map includes all selected layers
        def all_layers_present(cached_map, selected_layers):
            return all(any(layer_name in str(child) for child in cached_map._children.values()) for layer_name in selected_layers)

        map_exists = cache_key in st.session_state.map_cache
        cached_map = st.session_state.map_cache.get(cache_key) if map_exists else None

        should_rebuild = (
            not map_exists
            or selected_layers != st.session_state.get("last_layer_selection", [])
            or not all_layers_present(cached_map, selected_layers)
        )

        if selected_layers:
            if should_rebuild:
                with st.spinner("Loading map layers..."):
                    try:
                        m = folium.Map(
                            location=[33.886297, -84.362697],
                            zoom_start=9,
                            tiles="cartodbpositron",
                            prefer_canvas=True
                        )

                        for layer_name in selected_layers:
                            gdf = get_map_layer_data(layer_name)
                            if gdf is None or gdf.empty:
                                continue

                            if layer_name == "Applicant Locations":
                                add_coloured_markers_to_map(
                                    folium_map=m,
                                    gdf=gdf,
                                    lat_col="lat",
                                    lon_col="lon",
                                    colour_by="status",
                                    layer_name="Applicant Locations",
                                    clustered=False,
                                    categorical_colours=status_colours
                                )
                            elif layer_name == "Total Score":
                                layer, legend = add_lat_lon_score_layer(
                                    gdf, "Total Score", "score", YlGnBu_20, 4, max_points
                                )
                                layer.add_to(m)
                                if legend:
                                    legend.add_to(m)
                            elif layer_name == "Desirable/Undesirable Activities Score":
                                layer, legend = add_lat_lon_score_layer(
                                    gdf, layer_name, "score", YlGnBu_20, 4, max_points
                                )
                                layer.add_to(m)
                                if legend:
                                    legend.add_to(m)
                            elif layer_name == "Community Transportation Score":
                                layer, legend = add_lat_lon_score_layer(
                                    gdf, layer_name, "score", YlGnBu_5, 4, max_points
                                )
                                layer.add_to(m)
                                if legend:
                                    legend.add_to(m)
                            elif layer_name == "Stable Communities Score":
                                add_tract_score_layer_stable(
                                    m, gdf, "score", layer_name, simplify_tolerance=0.005
                                )
                            elif layer_name == "Quality Education Score":
                                layer = add_tract_score_layer(
                                    m, gdf, "score", layer_name, simplify_tolerance=0.005
                                )
                                if layer:
                                    layer.add_to(m)

                        st.session_state.map_cache[cache_key] = m

                    except Exception as e:
                        st.error(f"Error creating map: {str(e)}")
                        st.stop()

            st.session_state.last_layer_selection = selected_layers.copy()

            cached_map = st.session_state.map_cache[cache_key]

            if show_user_point and st.session_state.get("scores_calculated", False):
                import copy
                display_map = copy.deepcopy(cached_map)
                folium.Marker(
                    [st.session_state.latitude, st.session_state.longitude],
                    tooltip="Your Site",
                    popup=f"Total Score: {st.session_state.total_score:.2f}",
                    icon=folium.Icon(color="red", icon="star")
                ).add_to(display_map)
            else:
                display_map = cached_map

            st_folium(
                display_map,
                width=700,
                height=600,
                returned_objects=[],
                key=f"main_map_{hash(tuple(sorted(selected_layers)))}"
            )

        else:
            st.info("Select at least one layer to display the map.")



# with main_col2:

#     # === TABS FOR MAP DISPLAY ===
#     tab1, tab2, tab3 = st.tabs([
#         "Location Criteria Score Map",
#         "Stable Communities Indicator Map",
#         "Housing Needs Indicator Map"
#     ])

#     with tab1:
#         st.markdown("#### Map of Selected Layers")
#         selected_layers = st.multiselect(
#             "Choose layers to display:",
#             options=[
#                 "Total Score", 
#                 "Desirable/Undesirable Activities Score", 
#                 "Community Transportation Score",
#                 "Stable Communities Score",
#                 "Quality Education Score", 
#                 "Applicant Locations"
#             ],
#             default=["Total Score"],
#             key="layer_selection"
#         )

#         # Control for lat/lon score layers sampling
#         if any("Score" in layer and layer != "Applicant Locations" for layer in selected_layers):
#             max_points = st.slider(
#                 "Max points for score layers (for performance tuning)",
#                 min_value=2000,
#                 max_value=13000,
#                 value=1000,
#                 step=500,
#                 help="Controls how many points are shown for lat/lon score layers. Higher = more detail, lower = better performance."
#             )
#         else:
#             max_points = 2000  

#         # Map controls
#         show_user_point = st.checkbox(
#             "Show Site on Map", 
#             value=False,
#             disabled=not (hasattr(st.session_state, 'scores_calculated') and st.session_state.scores_calculated)
#         )

#         # Compute a stable cache key
#         cache_key = f"{'-'.join(sorted(selected_layers))}_{max_points}"
#         map_exists = cache_key in st.session_state.map_cache
#         layers_changed = selected_layers != st.session_state.last_layer_selection
#         should_rebuild = selected_layers and (layers_changed or not map_exists)

#         # ✅ Only rebuild if layers are selected AND something changed
#         if selected_layers:
#             if should_rebuild:
#                 with st.spinner("Loading map layers..."):
#                     try:
#                         # Initialize base map
#                         center_lat = 33.886297
#                         center_lon = -84.362697
#                         m = folium.Map(
#                             location=[center_lat, center_lon], 
#                             zoom_start=9, 
#                             tiles="cartodbpositron",
#                             prefer_canvas=True
#                         )

#                         # Dynamically add layers
#                         for layer_name in selected_layers:
#                             gdf = get_map_layer_data(layer_name)
#                             if gdf is None or gdf.empty:
#                                 continue
                            
#                             if layer_name == "Applicant Locations":
#                                 add_coloured_markers_to_map(
#                                     folium_map=m,
#                                     gdf=gdf,
#                                     lat_col="lat",
#                                     lon_col="lon",
#                                     colour_by="status",
#                                     layer_name="Applicant Locations",
#                                     clustered=False,
#                                     categorical_colours=status_colours
#                                 )
#                             elif layer_name == "Total Score":
#                                 layer, legend = add_lat_lon_score_layer(
#                                     gdf, layer_name="Total Score", score_column="score",
#                                     palette=YlGnBu_20, radius=4, max_points=max_points
#                                 )
#                                 layer.add_to(m)
#                                 if legend:
#                                     legend.add_to(m)
#                             elif layer_name == "Desirable/Undesirable Activities Score":
#                                 layer, legend = add_lat_lon_score_layer(
#                                     gdf, layer_name="Desirable/Undesirable Activities Score", score_column="score",
#                                     palette=YlGnBu_20, radius=4, max_points=max_points
#                                 )
#                                 layer.add_to(m)
#                                 if legend:
#                                     legend.add_to(m)
#                             elif layer_name == "Community Transportation Score":
#                                 layer, legend = add_lat_lon_score_layer(
#                                     gdf, layer_name="Community Transportation Score", score_column="score",
#                                     palette=YlGnBu_5, radius=4, max_points=max_points
#                                 )
#                                 layer.add_to(m)
#                                 if legend:
#                                     legend.add_to(m)
#                             elif layer_name == "Stable Communities Score":
#                                 add_tract_score_layer_stable(
#                                     m, gdf, score_column="score", layer_name="Stable Communities Score", simplify_tolerance=0.005
#                                 )
#                             elif layer_name == "Quality Education Score":
#                                 layer = add_tract_score_layer(
#                                     m, gdf, score_column="score", layer_name="Quality Education Score", simplify_tolerance=0.005
#                                 )
#                                 if layer:
#                                     layer.add_to(m)

#                         # ✅ Cache and update state
#                         st.session_state.map_cache[cache_key] = m
#                         st.session_state.last_layer_selection = selected_layers.copy()

#                     except Exception as e:
#                         st.error(f"Error creating map: {str(e)}")
#                         st.stop()

#             # ✅ Retrieve from cache
#             cached_map = st.session_state.map_cache[cache_key]

#             # ✅ Add user marker if applicable
#             if (
#                 show_user_point and 
#                 st.session_state.get("scores_calculated", False)
#             ):
#                 import copy
#                 display_map = copy.deepcopy(cached_map)
#                 folium.Marker(
#                     [st.session_state.latitude, st.session_state.longitude], 
#                     tooltip="Your Site",
#                     popup=f"Total Score: {st.session_state.total_score:.2f}",
#                     icon=folium.Icon(color='red', icon='star')
#                 ).add_to(display_map)
#             else:
#                 display_map = cached_map

#             # ✅ Display the map
#             stable_key = f"main_map_{hash(tuple(sorted(selected_layers)))}"
#             map_data = st_folium(
#                 display_map, 
#                 width=700, 
#                 height=600,
#                 returned_objects=[],
#                 key=stable_key
#             )

#         else:
#             st.info("Select at least one layer to display the map.")

        # # Only render map if layers are selected
        # if selected_layers:
        #     # Check if layer selection changed
        #     layers_changed = selected_layers != st.session_state.last_layer_selection
            
        #     # Create cache key for map stability
        #     cache_key = f"{'-'.join(sorted(selected_layers))}_{max_points}"
            
        #     # Only rebuild when layers or max_points actually change
        #     if layers_changed or cache_key not in st.session_state.map_cache:
        #         with st.spinner("Loading map layers..."):
        #             try:
        #                 # Initialize map
        #                 center_lat = 33.886297
        #                 center_lon = -84.362697
        #                 m = folium.Map(
        #                     location=[center_lat, center_lon], 
        #                     zoom_start=9, 
        #                     tiles="cartodbpositron",
        #                     prefer_canvas=True
        #                 )

        #                 # Add layers dynamically - only load what's needed
        #                 for layer_name in selected_layers:
        #                     gdf = get_map_layer_data(layer_name)
        #                     if gdf is None or gdf.empty:
        #                         continue
                                
        #                     if layer_name == "Applicant Locations":
        #                         add_coloured_markers_to_map(
        #                             folium_map=m,
        #                             gdf=gdf,
        #                             lat_col="lat",
        #                             lon_col="lon",
        #                             colour_by="status",
        #                             layer_name="Applicant Locations",
        #                             clustered=False,  
        #                             categorical_colours=status_colours
        #                         )
        #                     elif layer_name == "Total Score":
        #                         layer, legend = add_lat_lon_score_layer(
        #                             gdf,
        #                             layer_name="Total Score",
        #                             score_column="score",
        #                             palette=YlGnBu_20,
        #                             radius=4,
        #                             max_points=max_points  
        #                         )
        #                         layer.add_to(m)
        #                         if legend:
        #                             legend.add_to(m)
        #                     elif layer_name == "Desirable/Undesirable Activities Score":
        #                         layer, legend = add_lat_lon_score_layer(
        #                             gdf,
        #                             layer_name="Desirable/Undesirable Activities Score",
        #                             score_column="score",
        #                             palette=YlGnBu_20,
        #                             radius=4,
        #                             max_points=max_points  
        #                         )
        #                         layer.add_to(m)
        #                         if legend:
        #                             legend.add_to(m)
        #                     elif layer_name == "Community Transportation Score":
        #                         layer, legend = add_lat_lon_score_layer(
        #                             gdf,
        #                             layer_name="Community Transportation Score",
        #                             score_column="score",
        #                             palette=YlGnBu_5,
        #                             radius=4,
        #                             max_points=max_points
        #                         )
        #                         layer.add_to(m)
        #                         if legend:
        #                             legend.add_to(m)
        #                     elif layer_name == "Stable Communities Score":
        #                         add_tract_score_layer_stable(
        #                             m,
        #                             gdf,
        #                             score_column="score",
        #                             layer_name="Stable Communities Score",
        #                             simplify_tolerance=0.005
        #                         )
        #                     elif layer_name == "Quality Education Score":
        #                         layer = add_tract_score_layer(
        #                             m,
        #                             gdf,
        #                             score_column="score",
        #                             layer_name="Quality Education Score",
        #                             simplify_tolerance=0.005
        #                         )
        #                         if layer:
        #                             layer.add_to(m)

        #                 # Cache the map
        #                 st.session_state.map_cache[cache_key] = m
        #                 st.session_state.last_layer_selection = selected_layers.copy()
                        
        #             except Exception as e:
        #                 st.error(f"Error creating map: {str(e)}")
        #                 st.stop()

        #     # Get the cached map
        #     if cache_key in st.session_state.map_cache:
        #         cached_map = st.session_state.map_cache[cache_key]
        #     else:
        #         st.warning("Map cache was cleared. Recreating map...")
        #         st.rerun()
            
        #     # Add user point if requested (without caching this change)
        #     if (show_user_point and 
        #         hasattr(st.session_state, 'scores_calculated') and 
        #         st.session_state.scores_calculated):
        #         # Create a copy of the cached map to add the user point
        #         import copy
        #         display_map = copy.deepcopy(cached_map)
        #         folium.Marker(
        #             [st.session_state.latitude, st.session_state.longitude], 
        #             tooltip="Your Site",
        #             popup=f"Total Score: {st.session_state.total_score:.2f}",
        #             icon=folium.Icon(color='red', icon='star')
        #         ).add_to(display_map)
        #     else:
        #         display_map = cached_map

        #     # Display the map - NO returned objects to prevent grey-out
        #     stable_key = f"main_map_{hash(tuple(sorted(selected_layers)))}"
            
        #     map_data = st_folium(
        #         display_map, 
        #         width=700, 
        #         height=600,
        #         returned_objects=[],
        #         key=stable_key
        #     )
        # else:
        #     st.info("Select layers above to display the map.")

    with tab2:
        st.markdown("#### Stable Communities Indicators")
        st.info("Select indicators and click 'Load Map' to display stable communities data.")

    with tab3:
        st.markdown("#### Housing Needs Indicator Map") 
        st.info("Click 'Load Map' to display housing needs data.")