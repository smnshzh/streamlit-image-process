import streamlit as st
from streamlit_folium import st_folium
import folium
from geopy.distance import geodesic

# Predefined billboard locations
billboard_locations = {
    "Billboard 1": (35.6892, 51.3890),  # Example coordinates (Tehran)
    "Billboard 2": (35.7156, 51.4027),  # Example coordinates (Tehran)
}

# Title
st.title("Treasure Hunt App")

# Header
st.header("Step 1: Select Your Location")

# Initialize map centered at a default location
default_location = (35.6892, 51.3890)  # Tehran
m = folium.Map(location=default_location, zoom_start=12)

# Add billboard locations to the map
for name, location in billboard_locations.items():
    folium.Marker(location, popup=name, icon=folium.Icon(color="red")).add_to(m)

# Add an interactive marker for user to select location
user_marker = folium.Marker(
    location=default_location,
    draggable=True,
    popup="Drag me to your location!",
    icon=folium.Icon(color="blue"),
)
user_marker.add_to(m)

# Render the map in the Streamlit app
map_data = st_folium(m, width=700, height=500)

# Get user's geolocation using JavaScript for the browser's geolocation API
st.markdown("""
<script>
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            window.parent.postMessage({
                'type': 'streamlit:set_component_value',
                'id': 'user_location',
                'value': {
                    'latitude': position.coords.latitude,
                    'longitude': position.coords.longitude
                }
            }, '*');
        }, function(error) {
            window.parent.postMessage({
                'type': 'streamlit:set_component_value',
                'id': 'error_message',
                'value': 'Unable to get your location. Please check your browser settings.'
            }, '*');
        });
    } else {
        window.parent.postMessage({
            'type': 'streamlit:set_component_value',
            'id': 'error_message',
            'value': 'Geolocation is not supported by this browser.'
        }, '*');
    }
</script>
""", unsafe_allow_html=True)

# Receive the user's location or error message
user_location = st.session_state.get('user_location')
error_message = st.session_state.get('error_message')

if error_message:
    st.error(error_message)
elif user_location:
    latitude, longitude = user_location['latitude'], user_location['longitude']
    st.success(f"Your current location: Latitude {latitude}, Longitude {longitude}")

    # Add user's location to the map
    folium.Marker(
        location=(latitude, longitude),
        popup="Your location",
        icon=folium.Icon(color="green"),
    ).add_to(m)

    # Check proximity to billboards
    st.header("Step 2: Check Proximity")
    found = False
    for name, location in billboard_locations.items():
        distance = geodesic((latitude, longitude), location).meters
        if distance < 100:  # Example threshold for proximity (100 meters)
            found = True
            st.success(f"You are near {name}! Proceed to scan the billboard.")
            break

    if not found:
        st.error("You are not near any billboard. Please move closer.")
else:
    st.warning("Waiting to retrieve your location. Please ensure location services are enabled.")
