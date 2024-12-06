import streamlit as st
from streamlit_folium import st_folium
import folium

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

# Check if user has selected a location
if map_data and "last_clicked" in map_data:
    user_location = map_data["last_clicked"]
    latitude, longitude = user_location["lat"], user_location["lng"]
    st.success(f"Your selected location: Latitude {latitude}, Longitude {longitude}")

    # Check proximity to billboards
    st.header("Step 2: Check Proximity")
    found = False
    for name, location in billboard_locations.items():
        distance = ((latitude - location[0]) ** 2 + (longitude - location[1]) ** 2) ** 0.5
        if distance < 0.01:  # Example threshold for proximity
            found = True
            st.success(f"You are near {name}! Proceed to scan the billboard.")
            break

    if not found:
        st.error("You are not near any billboard. Please move closer.")
else:
    st.warning("Drag the blue marker to your location and click on the map to confirm.")
