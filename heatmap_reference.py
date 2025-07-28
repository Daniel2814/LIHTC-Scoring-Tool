"""
REFERENCE CODE: Heatmap Visualization for Stable Communities Maps
================================================================

This file contains reference code for implementing smoothed gradient heatmap
visualizations instead of polygon-based choropleth maps for Stable Communities
indicators. This code is for reference only and not actively used.

Author: Emory Center for AI
Date: July 2025
Purpose: Convert polygon-based tract maps to heatmap-style visualizations

IMPLEMENTATION NOTES:
- Add this function to map_layers/build_layers.py
- Replace calls to add_tract_score_layer_stable() with add_heatmap_layer()
- Requires folium plugins import: from folium import plugins
- May need additional dependencies: scipy for interpolation

"""

import folium
from folium import plugins
import pandas as pd
import numpy as np

def add_heatmap_layer(folium_map, gdf, score_column, layer_name, radius=25, blur=15, gradient=None):
    """
    Add a heatmap layer to the folium map using polygon centroids and scores
    
    Creates a smoothed gradient heatmap instead of discrete polygon boundaries.
    Converts census tract polygons to centroid points with intensity values.
    
    Args:
        folium_map: folium.Map object to add the layer to
        gdf: GeoDataFrame with polygon geometry and a score column
        score_column: name of the column to use for heat values
        layer_name: name of the layer shown in the layer control
        radius: radius of each heat point in pixels (default: 25)
        blur: blur factor for smoothing effect (default: 15)
        gradient: custom color gradient dict (optional)
    
    Returns:
        None (modifies folium_map in place)
    
    Example Usage:
        # Replace this:
        add_tract_score_layer_stable(m, gdf, "score", "Stable Communities Score")
        
        # With this:
        add_heatmap_layer(m, gdf, "score", "Stable Communities Score", radius=30, blur=20)
    """
    
    # Ensure CRS is EPSG:4326 for folium compatibility
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    
    # Clean and validate score data
    gdf[score_column] = pd.to_numeric(gdf[score_column], errors="coerce")
    gdf = gdf.dropna(subset=[score_column])
    
    if gdf.empty:
        print(f"Warning: No valid data for {layer_name}")
        return
    
    # Calculate polygon centroids for heatmap points
    gdf['centroid'] = gdf.geometry.centroid
    gdf['lat'] = gdf['centroid'].y
    gdf['lon'] = gdf['centroid'].x
    
    # Normalize scores to 0-1 range for heatmap intensity
    min_score = gdf[score_column].min()
    max_score = gdf[score_column].max()
    
    if max_score == min_score:
        # Handle case where all scores are identical
        gdf['intensity'] = 0.5
    else:
        gdf['intensity'] = (gdf[score_column] - min_score) / (max_score - min_score)
    
    # Prepare heatmap data: [latitude, longitude, weight]
    heat_data = []
    for _, row in gdf.iterrows():
        heat_data.append([row['lat'], row['lon'], row['intensity']])
    
    # Define default color gradient for stable communities
    if gradient is None:
        gradient = {
            0.0: 'blue',     # Low values - blue
            0.2: 'cyan',     # 
            0.4: 'lime',     # Medium-low - green
            0.6: 'yellow',   # Medium-high - yellow
            0.8: 'orange',   # High - orange
            1.0: 'red'       # Highest values - red
        }
    
    # Create and configure heatmap layer
    heatmap = plugins.HeatMap(
        heat_data,
        name=layer_name,
        radius=radius,           # Size of heat points
        blur=blur,               # Smoothing factor
        gradient=gradient,       # Color scheme
        min_opacity=0.3,         # Minimum transparency
        max_zoom=18,             # Maximum zoom level
        show=True                # Show by default
    )
    
    # Add heatmap to the map
    heatmap.add_to(folium_map)
    
    # Create custom legend for the heatmap
    legend_html = f"""
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px; border-radius: 5px;">
    <p><strong>{layer_name}</strong></p>
    <p>Range: {min_score:.2f} - {max_score:.2f}</p>
    <div style="display: flex; align-items: center; margin: 5px 0;">
        <div style="width: 100px; height: 15px; 
                    background: linear-gradient(to right, blue, cyan, lime, yellow, orange, red); 
                    margin-right: 5px; border: 1px solid #ccc;"></div>
    </div>
    <p style="font-size: 12px; margin: 0;"><span style="float: left;">Low</span><span style="float: right;">High</span></p>
    </div>
    """
    
    # Add legend to map
    folium_map.get_root().html.add_child(folium.Element(legend_html))
    
    print(f"Added heatmap layer: {layer_name} with {len(heat_data)} points")
    print(f"Score range: {min_score:.2f} to {max_score:.2f}")


# ALTERNATIVE GRADIENT CONFIGURATIONS
# ===================================

def get_custom_gradients():
    """
    Returns dictionary of custom color gradients for different indicators
    """
    return {
        'stable_communities': {
            0.0: 'red',      # Poor stability
            0.5: 'yellow',   # Moderate stability  
            1.0: 'green'     # High stability
        },
        
        'environmental_health': {
            0.0: 'purple',   # Poor environmental health
            0.3: 'blue',
            0.6: 'cyan',
            1.0: 'white'     # Excellent environmental health
        },
        
        'income': {
            0.0: 'darkred',  # Low income
            0.25: 'red',
            0.5: 'orange',
            0.75: 'yellow',
            1.0: 'green'     # High income
        },
        
        'poverty': {
            0.0: 'green',    # Low poverty (good)
            0.5: 'yellow',
            1.0: 'red'       # High poverty (concerning)
        }
    }


# IMPLEMENTATION IN SCORING_TOOL.PY
# =================================

"""
To implement this heatmap functionality, replace the current Stable Communities
map rendering sections in scoring_tool.py with the following code:

STEP 1: Add import to map_layers/build_layers.py
-------
from folium import plugins

STEP 2: Add the add_heatmap_layer function to map_layers/build_layers.py
-------
# Copy the add_heatmap_layer function above into build_layers.py

STEP 3: Replace map rendering code in scoring_tool.py (around lines 780-810)
-------

# Current code (polygons):
elif layer_name == "Stable Communities Score":
    add_tract_score_layer_stable(
        m, gdf, "score", "Stable Communities Score", simplify_tolerance=0.005
    )

# Replace with (heatmap):
elif layer_name == "Stable Communities Score":
    add_heatmap_layer(
        m, gdf, "score", "Stable Communities Score", radius=30, blur=20
    )

# Apply similar changes for other stable community indicators:
elif layer_name == "Environmental Health Index":
    add_heatmap_layer(
        m, gdf, "Environmental Health Index", layer_name, radius=30, blur=20
    )

elif layer_name == "Median Income":
    gradient = {0.0: 'darkred', 0.5: 'yellow', 1.0: 'green'}
    add_heatmap_layer(
        m, gdf, "Median Income", layer_name, radius=30, blur=20, gradient=gradient
    )

# etc. for other indicators...

STEP 4: Performance Considerations
-------
- Heatmaps render faster than complex polygons
- Reduce radius/blur values if performance is an issue
- Consider caching heatmap data for frequently accessed layers
- Test with different zoom levels to ensure readability

STEP 5: Customization Options
-------
- radius: 15-50 pixels (smaller = more precise, larger = smoother)
- blur: 10-30 pixels (higher = more blended)
- gradient: customize colors for different data types
- min_opacity: 0.1-0.5 (lower = more transparent)

"""

# TESTING AND VALIDATION
# ======================

def test_heatmap_implementation():
    """
    Test function to validate heatmap implementation
    This would be used during development to ensure the heatmap works correctly
    """
    
    # Test data structure
    test_requirements = {
        'gdf_requirements': [
            'Must have geometry column with polygons',
            'Must have score column with numeric values',
            'CRS should be convertible to EPSG:4326'
        ],
        
        'output_validation': [
            'Heatmap layer added to folium map',
            'Legend displays correct score range',
            'Heat points correspond to polygon centroids',
            'Intensity values properly normalized 0-1'
        ],
        
        'performance_targets': [
            'Render time < 2 seconds for 500 polygons',
            'Smooth interaction at zoom levels 8-15',
            'Memory usage < 50MB for typical dataset'
        ]
    }
    
    return test_requirements


# END OF REFERENCE CODE
# ====================

"""
This reference implementation provides:

1. Complete heatmap function with documentation
2. Custom gradient examples for different data types  
3. Step-by-step implementation instructions
4. Performance and customization guidelines
5. Testing framework outline

The heatmap approach offers several advantages over polygon choropleth:
- Smoother, more visually appealing gradients
- Better performance with large datasets
- More intuitive heat-style visualization
- Reduced visual clutter from polygon boundaries
- Easier to identify hot spots and patterns

To activate this code, copy the add_heatmap_layer function to build_layers.py
and update the map rendering logic in scoring_tool.py as indicated above.
"""
