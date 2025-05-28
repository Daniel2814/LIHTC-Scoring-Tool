# ## build_layers.py

# import pandas as pd
# import geopandas as gpd
# from shapely.geometry import Point
# import folium
# from folium import CircleMarker, GeoJson, GeoJsonTooltip, FeatureGroup, LayerControl
# from folium.plugins import MarkerCluster
# import branca.colormap as cm
# from branca.colormap import linear


# #################################################################################################
# # Build circle layer for lat/lon points 
# def add_lat_lon_score_layer(gdf, layer_name, score_column="score", palette=None, radius=3):
#     """
#     Adds a CircleMarker layer to a Folium map using actual scores for colour mapping.

#     Args:
#         gdf (GeoDataFrame): Must contain geometry and a numeric score column.
#         layer_name (str): Name for the layer.
#         score_column (str): Name of the column containing numeric scores.
#         palette (list): List of hex colours (e.g., YlGnBu_20).
#         radius (int): Circle radius in pixels.

#     Returns:
#         A tuple: (FeatureGroup layer, colourmap)
#     """
#     # Filter out rows with missing geometry or score
#     valid_gdf = gdf[~gdf.geometry.is_empty & gdf.geometry.notnull()].copy()
#     valid_gdf = valid_gdf[valid_gdf[score_column].notnull()]
    
#     if valid_gdf.empty:
#         return folium.FeatureGroup(name=layer_name), None

#     # Create colourmap using the score range and your custom palette
#     colourmap = cm.LinearColormap(
#         colors=palette,
#         vmin=valid_gdf[score_column].min(),
#         vmax=valid_gdf[score_column].max(),
#         caption=layer_name
#     )

#     # Create a FeatureGroup to hold the markers
#     layer = folium.FeatureGroup(name=layer_name)

#     # Add each point as a circle marker
#     for _, row in valid_gdf.iterrows():
#         lat = row.geometry.y
#         lon = row.geometry.x
#         score = row[score_column]
#         colour = colourmap(score)

#         CircleMarker(
#             location=[lat, lon],
#             radius=radius,
#             color=colour,
#             weight = 0.1,
#             fill=True,
#             fill_color=colour,
#             fill_opacity=0.4,
#             popup=f"{score_column.title()}: {score:.2f}"
#         ).add_to(layer)

#     return layer, colourmap

# ##################################################################################################
# # Build heat map layer for census tract level 
# def add_tract_score_layer_stable(folium_map, gdf, score_column, layer_name, color_scheme="YlGnBu_09"):
#     """
#     Adds a choropleth-style layer to a Folium map using polygon scores.

#     Args:
#         folium_map: folium.Map object
#         gdf: GeoDataFrame with polygon geometry and a score column
#         score_column: name of the column to color by
#         layer_name: name of the layer shown in the layer control
#         color_scheme: color palette name from branca.linear (default: YlGnBu_09)
#     """
#     # Ensure CRS is EPSG:4326 for folium
#     gdf = gdf.to_crs("EPSG:4326")
#     gdf[score_column] = pd.to_numeric(gdf[score_column], errors="coerce")
#     print(gdf[score_column].head())
#     # Get color scale
#     vals = gdf[score_column].dropna()
#     if vals.empty:
#         print(f"No valid numeric values for '{score_column}' — skipping layer: {layer_name}")
#         return

#     # Proceed only if there are numeric values left
#     if len(vals) == 0:
#         print(f"No valid numeric values for '{score_column}' — skipping layer: {layer_name}")
#         return
#     print("Unique geometry types →", gdf.geom_type.unique())

#     cmap = getattr(linear, color_scheme).scale(vals.min(), vals.max())
#     cmap.caption = layer_name

#     # Add GeoJSON layer
#     folium.GeoJson(
#         gdf,
#         name=layer_name,
#         style_function=lambda feature: {
#             "fillColor": cmap(feature["properties"][score_column]) if feature["properties"][score_column] is not None else "#d3d3d3",
#             "color": "gray",
#             "weight": 1,
#             "fillOpacity": 0.8
#         },
#         tooltip=folium.features.GeoJsonTooltip(
#             fields=["GEOID", score_column],
#             aliases=["Tract", layer_name],
#             localize=True
#         ),
#         options={"name": layer_name}
#     ).add_to(folium_map)

#     # Add legend
#     cmap.add_to(folium_map)
    
# #----------------------------------------------------------------------------#

# def add_tract_score_layer(folium_map, gdf, score_column, layer_name, color_scheme="YlGnBu_09"):
#     """
#     Adds a choropleth-style layer to a Folium map using polygon scores.

#     Args:
#         folium_map: folium.Map object
#         gdf: GeoDataFrame with polygon geometry and a score column
#         score_column: name of the column to color by
#         layer_name: name of the layer shown in the layer control
#         color_scheme: color palette name from branca.linear (default: YlGnBu_09)
#     """
#     # Ensure CRS is EPSG:4326 for folium
#     gdf = gdf.to_crs("EPSG:4326")
#     gdf[score_column] = pd.to_numeric(gdf[score_column], errors="coerce")
#     print(gdf[score_column].head())
#     # Get color scale
#     vals = gdf[score_column].dropna()
#     if vals.empty:
#         print(f"No valid numeric values for '{score_column}' — skipping layer: {layer_name}")
#         return

#     # Proceed only if there are numeric values left
#     if len(vals) == 0:
#         print(f"No valid numeric values for '{score_column}' — skipping layer: {layer_name}")
#         return
#     print("Unique geometry types →", gdf.geom_type.unique())

#     cmap = getattr(linear, color_scheme).scale(vals.min(), vals.max())
#     cmap.caption = layer_name

#     # Add GeoJSON layer
#     folium.GeoJson(
#         gdf,
#         name=layer_name,
#         style_function=lambda feature: {
#             "fillColor": cmap(feature["properties"][score_column]) if feature["properties"][score_column] is not None else "#d3d3d3",
#             "color": "gray",
#             "weight": 0.3,
#             "fillOpacity": 0.8
#         },
#         tooltip=folium.features.GeoJsonTooltip(
#             fields=["GEOID", score_column],
#             aliases=["Tract", layer_name],
#             localize=True
#         ), 
#     ).add_to(folium_map)

#     # Add legend
#     cmap.add_to(folium_map)

# ##################################################################################################
# # Add point layers (applicants)
# def add_coloured_markers_to_map(
#     folium_map,
#     gdf,
#     lat_col="lat",
#     lon_col="lon",
#     colour_by=None,
#     popup_fields=None,
#     layer_name="Markers",
#     clustered=False,
#     categorical_colours=None,
# ):
#     """
#     Add color-coded markers to a folium map for categorical values.

#     Args:
#         folium_map: folium.Map object
#         gdf: GeoDataFrame or DataFrame
#         lat_col: column for latitude
#         lon_col: column for longitude
#         colour_by: column with categorical values to color by
#         popup_fields: list of columns to include in popup
#         layer_name: name of the feature group
#         clustered: whether to use MarkerCluster
#         categorical_colours: dict mapping category to color (optional)
#     """
#     feature_group = folium.FeatureGroup(name=layer_name)
#     if clustered:
#         marker_layer = MarkerCluster()
#     else:
#         marker_layer = folium.FeatureGroup(name=f"{layer_name} Markers")

#     if colour_by and categorical_colours is None:
#         # Auto-assign colors if not provided
#         unique_vals = gdf[colour_by].dropna().unique()
#         color_palette = ["green", "red", "blue", "orange", "purple", "gray"]
#         categorical_colours = {
#             val: color_palette[i % len(color_palette)]
#             for i, val in enumerate(sorted(unique_vals))
#         }

#     for _, row in gdf.iterrows():
#         lat = row[lat_col]
#         lon = row[lon_col]

#         if pd.isnull(lat) or pd.isnull(lon):
#             continue  

#         colour = "red"
#         if colour_by:
#             value = row.get(colour_by)
#             colour = categorical_colours.get(value, "red")

#         # Extract tooltip content
#         year = row.get("year", "")
#         dev_name = row.get("development_name", "")
#         owner_name = row.get("ownership_entity_name", "")
#         status = row.get("status", "Unknown")
#         dca_score = row.get("dca_score", "")

#         tooltip_text = (
#             f"<b>{dev_name}</b><br>"
#             f"Owner: {owner_name}<br>"
#             f"Year: {year}<br>"
#             f"Status: {status}<br>"
#             f"DCA Score: {dca_score}"
#         )

#         folium.CircleMarker(
#             location=(lat, lon),
#             radius=2,
#             color=colour,
#             fill=True,
#             fill_color=colour,
#             fill_opacity=1,
#             weight=0,
#             tooltip=folium.Tooltip(tooltip_text, sticky=True)  
#         ).add_to(marker_layer)

#     marker_layer.add_to(feature_group)
#     feature_group.add_to(folium_map)

# import pandas as pd
# import geopandas as gpd
# from shapely.geometry import Point
# import folium
# from folium import CircleMarker, GeoJson, GeoJsonTooltip, FeatureGroup, LayerControl
# from folium.plugins import MarkerCluster, FastMarkerCluster
# import branca.colormap as cm
# from branca.colormap import linear
# import numpy as np

# #################################################################################################
# # Optimized circle layer for lat/lon points 
# def add_lat_lon_score_layer(gdf, layer_name, score_column="score", palette=None, radius=3, max_points=13000):
#     """
#     Adds a CircleMarker layer to a Folium map using actual scores for colour mapping.
#     Optimized for performance with large datasets.

#     Args:
#         gdf (GeoDataFrame): Must contain geometry and a numeric score column.
#         layer_name (str): Name for the layer.
#         score_column (str): Name of the column containing numeric scores.
#         palette (list): List of hex colours (e.g., YlGnBu_20).
#         radius (int): Circle radius in pixels.
#         max_points (int): Maximum points to render (will sample if exceeded).

#     Returns:
#         A tuple: (FeatureGroup layer, colourmap)
#     """
#     # Early return for empty data
#     if gdf.empty:
#         return folium.FeatureGroup(name=layer_name), None
    
#     # Filter out rows with missing geometry or score
#     valid_gdf = gdf[~gdf.geometry.is_empty & gdf.geometry.notnull()].copy()
#     valid_gdf = valid_gdf[valid_gdf[score_column].notnull()]
    
#     if valid_gdf.empty:
#         return folium.FeatureGroup(name=layer_name), None

#     # Sample data if too many points for performance
#     if len(valid_gdf) > max_points:
#         valid_gdf = valid_gdf.sample(n=max_points, random_state=42)
    
#     # Ensure CRS is correct (do this once)
#     if valid_gdf.crs != "EPSG:4326":
#         valid_gdf = valid_gdf.to_crs("EPSG:4326")

#     # Pre-extract coordinates for efficiency
#     coords = [(geom.y, geom.x) for geom in valid_gdf.geometry]
#     scores = valid_gdf[score_column].values
    
#     # Create colourmap using the score range
#     score_min, score_max = scores.min(), scores.max()
#     if score_min == score_max:
#         # Handle case where all scores are the same
#         score_max = score_min + 1
        
#     colourmap = cm.LinearColormap(
#         colors=palette,
#         vmin=score_min,
#         vmax=score_max,
#         caption=layer_name
#     )

#     # Create a FeatureGroup to hold the markers
#     layer = folium.FeatureGroup(name=layer_name)

#     # Vectorized color mapping
#     colors = [colourmap(score) for score in scores]

#     # Add markers in batch (more efficient than individual adds)
#     for i, ((lat, lon), score, color) in enumerate(zip(coords, scores, colors)):
#         CircleMarker(
#             location=[lat, lon],
#             radius=radius,
#             color=color,
#             weight=0.1,
#             fill=True,
#             fill_color=color,
#             fill_opacity=0.4,
#             popup=f"{score_column.title()}: {score:.2f}"
#         ).add_to(layer)

#     return layer, colourmap

# ##################################################################################################
# # Optimized heat map layer for census tract level 
# def add_tract_score_layer_stable(folium_map, gdf, score_column, layer_name, color_scheme="YlGnBu_09", simplify_tolerance=0.001):
#     """
#     Adds a choropleth-style layer to a Folium map using polygon scores.
#     Optimized for performance with geometry simplification.

#     Args:
#         folium_map: folium.Map object
#         gdf: GeoDataFrame with polygon geometry and a score column
#         score_column: name of the column to color by
#         layer_name: name of the layer shown in the layer control
#         color_scheme: color palette name from branca.linear
#         simplify_tolerance: tolerance for geometry simplification (smaller = more detail)
#     """
#     if gdf.empty:
#         print(f"Empty geodataframe for layer: {layer_name}")
#         return
    
#     # Ensure CRS is EPSG:4326 for folium (do once)
#     if gdf.crs != "EPSG:4326":
#         gdf = gdf.to_crs("EPSG:4326")
    
#     # Clean and prepare score data
#     gdf = gdf.copy()
#     gdf[score_column] = pd.to_numeric(gdf[score_column], errors="coerce")
    
#     # Remove rows with invalid scores
#     valid_gdf = gdf[gdf[score_column].notnull()].copy()
    
#     if valid_gdf.empty:
#         print(f"No valid numeric values for '{score_column}' — skipping layer: {layer_name}")
#         return

#     # Simplify geometries for better performance
#     if simplify_tolerance > 0:
#         valid_gdf['geometry'] = valid_gdf['geometry'].simplify(tolerance=simplify_tolerance)
    
#     # Get color scale
#     vals = valid_gdf[score_column]
#     val_min, val_max = vals.min(), vals.max()
    
#     if val_min == val_max:
#         val_max = val_min + 1
    
#     cmap = getattr(linear, color_scheme).scale(val_min, val_max)
#     cmap.caption = layer_name

#     # Prepare data for efficient rendering
#     # Convert to GeoJSON format once
#     geojson_data = valid_gdf.to_json()

#     # Add GeoJSON layer with optimized style function
#     def style_function(feature):
#         score_val = feature["properties"].get(score_column)
#         if score_val is not None:
#             fill_color = cmap(score_val)
#         else:
#             fill_color = "#d3d3d3"
        
#         return {
#             "fillColor": fill_color,
#             "color": "gray",
#             "weight": 1,
#             "fillOpacity": 0.8
#         }

#     folium.GeoJson(
#         geojson_data,
#         name=layer_name,
#         style_function=style_function,
#         tooltip=folium.features.GeoJsonTooltip(
#             fields=["GEOID", score_column],
#             aliases=["Tract", layer_name],
#             localize=True
#         ),
#         options={"name": layer_name}
#     ).add_to(folium_map)

#     # Add legend
#     cmap.add_to(folium_map)

# #----------------------------------------------------------------------------#

# def add_tract_score_layer(folium_map, gdf, score_column, layer_name, color_scheme="YlGnBu_09", simplify_tolerance=0.001):
#     """
#     Adds a choropleth-style layer to a Folium map using polygon scores.
#     Optimized version of the standard tract layer.
#     """
#     if gdf.empty:
#         print(f"Empty geodataframe for layer: {layer_name}")
#         return folium.FeatureGroup(name=layer_name)
    
#     # Ensure CRS is EPSG:4326 for folium
#     if gdf.crs != "EPSG:4326":
#         gdf = gdf.to_crs("EPSG:4326")
    
#     # Clean score data
#     gdf = gdf.copy()
#     gdf[score_column] = pd.to_numeric(gdf[score_column], errors="coerce")
    
#     # Filter valid data
#     valid_gdf = gdf[gdf[score_column].notnull()].copy()
    
#     if valid_gdf.empty:
#         print(f"No valid numeric values for '{score_column}' — skipping layer: {layer_name}")
#         return folium.FeatureGroup(name=layer_name)

#     # Simplify geometries
#     if simplify_tolerance > 0:
#         valid_gdf['geometry'] = valid_gdf['geometry'].simplify(tolerance=simplify_tolerance)
    
#     # Color mapping
#     vals = valid_gdf[score_column]
#     val_min, val_max = vals.min(), vals.max()
    
#     if val_min == val_max:
#         val_max = val_min + 1
    
#     cmap = getattr(linear, color_scheme).scale(val_min, val_max)
#     cmap.caption = layer_name

#     # Create feature group
#     layer = folium.FeatureGroup(name=layer_name)

#     # Add GeoJSON layer
#     folium.GeoJson(
#         valid_gdf.to_json(),
#         style_function=lambda feature: {
#             "fillColor": cmap(feature["properties"][score_column]) if feature["properties"][score_column] is not None else "#d3d3d3",
#             "color": "gray",
#             "weight": 0.3,
#             "fillOpacity": 0.8
#         },
#         tooltip=folium.features.GeoJsonTooltip(
#             fields=["GEOID", score_column],
#             aliases=["Tract", layer_name],
#             localize=True
#         ),
#     ).add_to(layer)

#     # Add legend
#     cmap.add_to(folium_map)
    
#     return layer

# ##################################################################################################
# # Optimized point layers (applicants)
# def add_coloured_markers_to_map(
#     folium_map,
#     gdf,
#     lat_col="lat",
#     lon_col="lon",
#     colour_by=None,
#     popup_fields=None,
#     layer_name="Markers",
#     clustered=True,  # Default to True for better performance
#     categorical_colours=None,
#     max_markers=2000,  # Limit for performance
# ):
#     """
#     Add color-coded markers to a folium map for categorical values.
#     Optimized for performance with large datasets.

#     Args:
#         folium_map: folium.Map object
#         gdf: GeoDataFrame or DataFrame
#         lat_col: column for latitude
#         lon_col: column for longitude
#         colour_by: column with categorical values to color by
#         popup_fields: list of columns to include in popup
#         layer_name: name of the feature group
#         clustered: whether to use MarkerCluster (recommended for performance)
#         categorical_colours: dict mapping category to color
#         max_markers: maximum number of markers to display
#     """
#     if gdf.empty:
#         return
    
#     # Filter out rows with missing coordinates
#     valid_gdf = gdf.dropna(subset=[lat_col, lon_col]).copy()
    
#     if valid_gdf.empty:
#         return
    
#     # Sample if too many points
#     if len(valid_gdf) > max_markers:
#         valid_gdf = valid_gdf.sample(n=max_markers, random_state=42)
    
#     # Set up colors
#     if colour_by and categorical_colours is None:
#         unique_vals = valid_gdf[colour_by].dropna().unique()
#         color_palette = ["green", "red", "blue", "orange", "purple", "gray"]
#         categorical_colours = {
#             val: color_palette[i % len(color_palette)]
#             for i, val in enumerate(sorted(unique_vals))
#         }

#     # Create feature group and marker layer
#     feature_group = folium.FeatureGroup(name=layer_name)
    
#     if clustered:
#         # Use FastMarkerCluster for better performance
#         marker_layer = MarkerCluster(
#             name=f"{layer_name} Markers",
#             maxClusterRadius=50,
#             spiderfyOnMaxZoom=True
#         )
#     else:
#         marker_layer = folium.FeatureGroup(name=f"{layer_name} Markers")

#     # Pre-extract data for efficient processing
#     lats = valid_gdf[lat_col].values
#     lons = valid_gdf[lon_col].values
    
#     # Prepare colors
#     if colour_by:
#         colors = [categorical_colours.get(val, "red") for val in valid_gdf[colour_by].values]
#     else:
#         colors = ["red"] * len(valid_gdf)
    
#     # Pre-prepare tooltip data
#     tooltip_data = []
#     for _, row in valid_gdf.iterrows():
#         year = row.get("year", "")
#         dev_name = row.get("development_name", "")
#         owner_name = row.get("ownership_entity_name", "")
#         status = row.get("status", "Unknown")
#         dca_score = row.get("dca_score", "")

#         tooltip_text = (
#             f"<b>{dev_name}</b><br>"
#             f"Owner: {owner_name}<br>"
#             f"Year: {year}<br>"
#             f"Status: {status}<br>"
#             f"DCA Score: {dca_score}"
#         )
#         tooltip_data.append(tooltip_text)

#     # Add markers efficiently
#     for lat, lon, color, tooltip_text in zip(lats, lons, colors, tooltip_data):
#         folium.CircleMarker(
#             location=(lat, lon),
#             radius=2,
#             color=color,
#             fill=True,
#             fill_color=color,
#             fill_opacity=1,
#             weight=0,
#             tooltip=folium.Tooltip(tooltip_text, sticky=True)  
#         ).add_to(marker_layer)

#     marker_layer.add_to(feature_group)
#     feature_group.add_to(folium_map)

# ##################################################################################################
# # Additional utility functions for performance optimization

# def preprocess_geodataframe(gdf, simplify_tolerance=0.001, target_crs="EPSG:4326"):
#     """
#     Preprocess a GeoDataFrame for optimal map rendering performance.
    
#     Args:
#         gdf: Input GeoDataFrame
#         simplify_tolerance: Tolerance for geometry simplification
#         target_crs: Target coordinate reference system
    
#     Returns:
#         Preprocessed GeoDataFrame
#     """
#     if gdf.empty:
#         return gdf
    
#     # Convert CRS if needed
#     if gdf.crs != target_crs:
#         gdf = gdf.to_crs(target_crs)
    
#     # Simplify geometries
#     if simplify_tolerance > 0:
#         gdf['geometry'] = gdf['geometry'].simplify(tolerance=simplify_tolerance)
    
#     # Remove invalid geometries
#     gdf = gdf[gdf.geometry.is_valid]
    
#     return gdf

# # def sample_points_by_bounds(gdf, bounds, max_points=12000):
# #     """
# #     Sample points within map bounds for better performance.
    
# #     Args:
# #         gdf: GeoDataFrame with point geometries
# #         bounds: Map bounds as [min_lat, min_lon, max_lat, max_lon]
# #         max_points: Maximum number of points to return
    
# #     Returns:
# #         Sampled GeoDataFrame
# #     """
# #     if gdf.empty:
# #         return gdf
    
# #     # Filter by bounds
# #     min_lat, min_lon, max_lat, max_lon = bounds
# #     mask = (
# #         (gdf.geometry.y >= min_lat) & 
# #         (gdf.geometry.y <= max_lat) &
# #         (gdf.geometry.x >= min_lon) & 
# #         (gdf.geometry.x <= max_lon)
# #     )
# #     filtered_gdf = gdf[mask]
    
# #     # Sample if too many points
# #     if len(filtered_gdf) > max_points:
# #         filtered_gdf = filtered_gdf.sample(n=max_points, random_state=42)
    
# #     return filtered_gdf


import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium import CircleMarker, GeoJson, GeoJsonTooltip, FeatureGroup, LayerControl
from folium.plugins import MarkerCluster
import branca.colormap as cm
from branca.colormap import linear

#################################################################################################
# Build circle layer for lat/lon points - WITH max_points parameter for user control
def add_lat_lon_score_layer(gdf, layer_name, score_column="score", palette=None, radius=3, max_points=800):
    """
    Adds a CircleMarker layer to a Folium map using actual scores for colour mapping.
    NOW with user-controllable max_points for performance tuning.

    Args:
        gdf (GeoDataFrame): Must contain geometry and a numeric score column.
        layer_name (str): Name for the layer.
        score_column (str): Name of the column containing numeric scores.
        palette (list): List of hex colours (e.g., YlGnBu_20).
        radius (int): Circle radius in pixels.
        max_points (int): Maximum points to render (user controllable).

    Returns:
        A tuple: (FeatureGroup layer, colourmap)
    """
    # Filter out rows with missing geometry or score
    valid_gdf = gdf[~gdf.geometry.is_empty & gdf.geometry.notnull()].copy()
    valid_gdf = valid_gdf[valid_gdf[score_column].notnull()]
    
    if valid_gdf.empty:
        return folium.FeatureGroup(name=layer_name), None

    # Sample data if too many points (stratified sampling to preserve distribution)
    if len(valid_gdf) > max_points:
        valid_gdf = valid_gdf.sample(n=max_points, random_state=42)

    # Create colourmap using the score range and your custom palette
    colourmap = cm.LinearColormap(
        colors=palette,
        vmin=valid_gdf[score_column].min(),
        vmax=valid_gdf[score_column].max(),
        caption=layer_name
    )

    # Create a FeatureGroup to hold the markers
    layer = folium.FeatureGroup(name=layer_name)

    # Add each point as a circle marker (keeping original style)
    for _, row in valid_gdf.iterrows():
        lat = row.geometry.y
        lon = row.geometry.x
        score = row[score_column]
        colour = colourmap(score)

        CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=colour,
            weight=0.1,
            fill=True,
            fill_color=colour,
            fill_opacity=0.4,
            popup=f"{score_column.title()}: {score:.2f}"
        ).add_to(layer)

    return layer, colourmap

##################################################################################################
# Build heat map layer for census tract level - OPTIMIZED with tolerance
def add_tract_score_layer_stable(folium_map, gdf, score_column, layer_name, color_scheme="YlGnBu_09", simplify_tolerance=0.005):
    """
    Adds a choropleth-style layer to a Folium map using polygon scores.
    Optimized for performance with geometry simplification.

    Args:
        folium_map: folium.Map object
        gdf: GeoDataFrame with polygon geometry and a score column
        score_column: name of the column to color by
        layer_name: name of the layer shown in the layer control
        color_scheme: color palette name from branca.linear (default: YlGnBu_09)
        simplify_tolerance: tolerance for geometry simplification (default: 0.005)
    """
    # Ensure CRS is EPSG:4326 for folium (do once)
    gdf = gdf.to_crs("EPSG:4326")
    gdf[score_column] = pd.to_numeric(gdf[score_column], errors="coerce")
    print(gdf[score_column].head())
    
    # Get color scale
    vals = gdf[score_column].dropna()
    if vals.empty:
        print(f"No valid numeric values for '{score_column}' — skipping layer: {layer_name}")
        return

    # Proceed only if there are numeric values left
    if len(vals) == 0:
        print(f"No valid numeric values for '{score_column}' — skipping layer: {layer_name}")
        return
    print("Unique geometry types →", gdf.geom_type.unique())

    # Simplify geometries for better performance
    if simplify_tolerance > 0:
        gdf['geometry'] = gdf['geometry'].simplify(tolerance=simplify_tolerance, preserve_topology=False)
        # Remove invalid geometries created by simplification
        gdf = gdf[gdf.geometry.is_valid]

    cmap = getattr(linear, color_scheme).scale(vals.min(), vals.max())
    cmap.caption = layer_name

    # Add GeoJSON layer
    folium.GeoJson(
        gdf,
        name=layer_name,
        style_function=lambda feature: {
            "fillColor": cmap(feature["properties"][score_column]) if feature["properties"][score_column] is not None else "#d3d3d3",
            "color": "gray",
            "weight": 1,
            "fillOpacity": 0.8
        },
        tooltip=folium.features.GeoJsonTooltip(
            fields=["GEOID", score_column],
            aliases=["Tract", layer_name],
            localize=True
        ),
        options={"name": layer_name}
    ).add_to(folium_map)

    # Add legend
    cmap.add_to(folium_map)

#----------------------------------------------------------------------------#

def add_tract_score_layer(folium_map, gdf, score_column, layer_name, color_scheme="YlGnBu_09", simplify_tolerance=0.005):
    """
    Adds a choropleth-style layer to a Folium map using polygon scores.
    Optimized version with geometry simplification.

    Args:
        folium_map: folium.Map object
        gdf: GeoDataFrame with polygon geometry and a score column
        score_column: name of the column to color by
        layer_name: name of the layer shown in the layer control
        color_scheme: color palette name from branca.linear (default: YlGnBu_09)
        simplify_tolerance: tolerance for geometry simplification
    """
    # Ensure CRS is EPSG:4326 for folium
    gdf = gdf.to_crs("EPSG:4326")
    gdf[score_column] = pd.to_numeric(gdf[score_column], errors="coerce")
    print(gdf[score_column].head())
    
    # Get color scale
    vals = gdf[score_column].dropna()
    if vals.empty:
        print(f"No valid numeric values for '{score_column}' — skipping layer: {layer_name}")
        return

    # Proceed only if there are numeric values left
    if len(vals) == 0:
        print(f"No valid numeric values for '{score_column}' — skipping layer: {layer_name}")
        return
    print("Unique geometry types →", gdf.geom_type.unique())

    # Simplify geometries for better performance
    if simplify_tolerance > 0:
        gdf['geometry'] = gdf['geometry'].simplify(tolerance=simplify_tolerance, preserve_topology=False)
        # Remove invalid geometries created by simplification
        gdf = gdf[gdf.geometry.is_valid]

    cmap = getattr(linear, color_scheme).scale(vals.min(), vals.max())
    cmap.caption = layer_name

    # Create feature group
    layer = folium.FeatureGroup(name=layer_name)

    # Add GeoJSON layer
    folium.GeoJson(
        gdf,
        name=layer_name,
        style_function=lambda feature: {
            "fillColor": cmap(feature["properties"][score_column]) if feature["properties"][score_column] is not None else "#d3d3d3",
            "color": "gray",
            "weight": 0.3,
            "fillOpacity": 0.8
        },
        tooltip=folium.features.GeoJsonTooltip(
            fields=["GEOID", score_column],
            aliases=["Tract", layer_name],
            localize=True
        ), 
    ).add_to(layer)

    # Add legend
    cmap.add_to(folium_map)
    
    return layer

##################################################################################################
# Add point layers (applicants) - KEEP ORIGINAL BEHAVIOR
def add_coloured_markers_to_map(
    folium_map,
    gdf,
    lat_col="lat",
    lon_col="lon",
    colour_by=None,
    popup_fields=None,
    layer_name="Markers",
    clustered=False,  # Keep original default
    categorical_colours=None,
):
    """
    Add color-coded markers to a folium map for categorical values.
    KEEPING ORIGINAL BEHAVIOR - no clustering by default, original tooltips.

    Args:
        folium_map: folium.Map object
        gdf: GeoDataFrame or DataFrame
        lat_col: column for latitude
        lon_col: column for longitude
        colour_by: column with categorical values to color by
        popup_fields: list of columns to include in popup
        layer_name: name of the feature group
        clustered: whether to use MarkerCluster (keeping original default False)
        categorical_colours: dict mapping category to color (optional)
    """
    feature_group = folium.FeatureGroup(name=layer_name)
    if clustered:
        marker_layer = MarkerCluster()
    else:
        marker_layer = folium.FeatureGroup(name=f"{layer_name} Markers")

    if colour_by and categorical_colours is None:
        # Auto-assign colors if not provided
        unique_vals = gdf[colour_by].dropna().unique()
        color_palette = ["green", "red", "blue", "orange", "purple", "gray"]
        categorical_colours = {
            val: color_palette[i % len(color_palette)]
            for i, val in enumerate(sorted(unique_vals))
        }

    for _, row in gdf.iterrows():
        lat = row[lat_col]
        lon = row[lon_col]

        if pd.isnull(lat) or pd.isnull(lon):
            continue  

        colour = "red"
        if colour_by:
            value = row.get(colour_by)
            colour = categorical_colours.get(value, "red")

        # KEEP ORIGINAL tooltip content and styling
        year = row.get("year", "")
        dev_name = row.get("development_name", "")
        owner_name = row.get("ownership_entity_name", "")
        status = row.get("status", "Unknown")
        dca_score = row.get("dca_score", "")

        tooltip_text = (
            f"<b>{dev_name}</b><br>"
            f"Owner: {owner_name}<br>"
            f"Year: {year}<br>"
            f"Status: {status}<br>"
            f"DCA Score: {dca_score}"
        )

        folium.CircleMarker(
            location=(lat, lon),
            radius=2,
            color=colour,
            fill=True,
            fill_color=colour,
            fill_opacity=1,
            weight=0,
            tooltip=folium.Tooltip(tooltip_text, sticky=True)  
        ).add_to(marker_layer)

    marker_layer.add_to(feature_group)
    feature_group.add_to(folium_map)
