import streamlit as st
import folium
import geojson
from folium.features import GeoJson
from streamlit_folium import folium_static  # Import folium_static

# Streamlit app title
st.title("GeoJSON Viewer and Editor")

# Upload GeoJSON file
uploaded_file = st.file_uploader("Upload a GeoJSON file", type=["geojson"])

if uploaded_file is not None:
    # Load the uploaded GeoJSON data
    geojson_data = geojson.load(uploaded_file)

    # Initializing Folium map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Function to change properties of GeoJSON features
    def style_function(feature):
        return {
            'fillColor': feature['properties'].get('marker-color', '#8C0D3E'),
            'color': feature['properties'].get('stork_x', '#000000'),
            'fillOpacity': 0.6,
            'weight': 2,
            'radius': 10 if feature['properties'].get('marker-size', 'small') == 'small' else 20
        }

    # Tooltip fields based on available data
    tooltip_fields = ['city', 'province', 'marker-size', 'marker-color']

    # Add GeoJSON data to the map with updated tooltip fields
    folium.GeoJson(
        geojson_data,
        name="geojson",
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=tooltip_fields),
    ).add_to(m)

    # Display map in Streamlit
    st.markdown("### Map with GeoJSON features:")
    folium_static(m)  # Display the Folium map

    # Allow the user to change the feature properties
    st.sidebar.header("Feature Properties Editor")
    
    for feature in geojson_data['features']:
        with st.sidebar.expander(f"Edit {feature['properties'].get('city', 'Feature')}"):
            # Change marker size
            marker_size = st.selectbox(
                "Marker Size", ["small", "large"], index=["small", "large"].index(feature['properties'].get('marker-size', 'small'))
            )
            feature['properties']["marker-size"] = marker_size

            # Change marker color
            marker_color = st.color_picker("Marker Color", value=feature['properties'].get("marker-color", "#8C0D3E"),key = "Marker Color")
            feature['properties']["marker-color"] = marker_color

            # Change stroke color
            stroke_color = st.color_picker("Stroke Color", value=feature['properties'].get("stork_x", "#000000"),key = "Stroke Color")
            feature['properties']["stork_x"] = stroke_color

            # Change icon
            icon_url = st.text_input(
                "Icon URL", value=feature['properties'].get("icon", "https://img.icons8.com/?size=100&id=104&format=png&color=000000")
            )
            feature['properties']["icon"] = icon_url

    # After editing, update the map and display it again
    folium_map = folium.Map(location=[20, 0], zoom_start=2)

    # Re-add the updated GeoJSON features
    folium.GeoJson(
        geojson_data,
        name="updated_geojson",
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=tooltip_fields),
    ).add_to(folium_map)

    # Display the updated map
    st.markdown("### Updated Map:")
    folium_static(folium_map)  # Display the updated Folium map
