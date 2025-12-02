import pydeck as pdk
import pandas as pd
import numpy as np

def render_3d_map(df):
    """
    Generates a PyDeck 3D Arc Layer map.
    Automatically assigns source coordinates to create arcs.
    """
    # 1. Prepare Data
    # The dataset usually has 'Latitude' and 'Longitude' for the Customer (Destination).
    # We need to simulate a "Source" (Warehouse) based on the Order Region to make the lines look real.
    
    # Define roughly where regional distribution centers might be
    warehouse_locs = {
        'Southeast Asia': {'lat': 13.75, 'lon': 100.50},
        'South Asia': {'lat': 20.59, 'lon': 78.96},
        'Oceania': {'lat': -25.27, 'lon': 133.77},
        'Eastern Asia': {'lat': 35.86, 'lon': 104.19},
        'West Asia': {'lat': 32.42, 'lon': 53.68},
        'West of USA': {'lat': 36.77, 'lon': -119.41},
        'US Center': {'lat': 37.09, 'lon': -95.71},
        'West Africa': {'lat': 9.08, 'lon': 8.67},
        'Central Africa': {'lat': 6.61, 'lon': 20.93},
        'North Africa': {'lat': 26.01, 'lon': 32.27},
        'Western Europe': {'lat': 46.22, 'lon': 2.21},
        'Northern Europe': {'lat': 60.47, 'lon': 8.46},
        'Southern Europe': {'lat': 41.87, 'lon': 12.56},
        'East of USA': {'lat': 40.71, 'lon': -74.00},
        'Canada': {'lat': 56.13, 'lon': -106.34},
        'Caribbean': {'lat': 21.46, 'lon': -78.65},
        'South America': {'lat': -14.23, 'lon': -51.92},
        'Central America': {'lat': 12.76, 'lon': -85.20}
    }

    # Helper function to get source lat
    def get_source_lat(region):
        return warehouse_locs.get(region, {'lat': 40.71, 'lon': -74.00})['lat']

    def get_source_lon(region):
        return warehouse_locs.get(region, {'lat': 40.71, 'lon': -74.00})['lon']

    # Apply coordinates (Limit to 2000 rows for performance)
    map_data = df.head(2000).copy()
    
    # Ensure columns exist
    if 'Order Region' in map_data.columns and 'Latitude' in map_data.columns:
        map_data['lat_source'] = map_data['Order Region'].apply(get_source_lat)
        map_data['lon_source'] = map_data['Order Region'].apply(get_source_lon)
        
        # Color Logic: Red for Late, Green for On Time
        # DataCo dataset uses 'Delivery Status'. 
        # Late delivery = 'Late delivery'
        map_data['color_r'] = map_data['Delivery Status'].apply(lambda x: 255 if x == 'Late delivery' else 0)
        map_data['color_g'] = map_data['Delivery Status'].apply(lambda x: 0 if x == 'Late delivery' else 255)
        map_data['color_b'] = 0 # Blue channel 0
    else:
        # Fallback if columns missing
        return None

    # 2. Define the Layer
    layer = pdk.Layer(
        "ArcLayer",
        data=map_data,
        get_source_position=["lon_source", "lat_source"],
        get_target_position=["Longitude", "Latitude"],
        get_source_color=["color_r", "color_g", "color_b", 150], # RGBA
        get_target_color=["color_r", "color_g", "color_b", 150],
        auto_highlight=True,
        width_scale=1,
        get_width=2,
        get_tilt=15,
    )

    # 3. Define the View
    view_state = pdk.ViewState(
        latitude=20, longitude=0, zoom=1.5, pitch=45, bearing=0
    )

    # 4. Render Deck
    return pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip={"text": "Order: {Order Id}\nStatus: {Delivery Status}\nProduct: {Product Name}"}
    )
