import streamlit as st
from streamlit_folium import st_folium
import folium

# Predefined billboard locations
billboard_locations = {
    "Billboard 1": (35.6892, 51.3890),  # Example coordinates (Tehran)
    "Billboard 2": (35.7156, 51.4027),  # Example coordinates (Tehran)
}

# JavaScript to get user location
def get_location_script():
    return """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude;
                    const long = position.coords.longitude;
                    const locationInput = document.getElementById("location");
                    locationInput.value = `${lat},${long}`;
                    locationInput.dispatchEvent(new Event('change'));
                },
                (error) => {
                    if (error.code === error.PERMISSION_DENIED) {
                        alert('Permission denied. Please allow location access in your browser settings.');
                    } else {
                        alert('Unable to retrieve location. Please try again.');
                    }
                }
            );
        } else {
            alert('Geolocation is not supported by your browser.');
        }
    }
    </script>
    """

# Add JavaScript for location retrieval
st.markdown(get_location_script(), unsafe_allow_html=True)

# Hidden input to receive location
location_input = st.text_input("Your Location", key="location", label_visibility="hidden")

# Button to trigger location retrieval
if st.button("Get My Location"):
    st.markdown('<script>getLocation();</script>', unsafe_allow_html=True)

# Check if location data is available
if location_input:
    latitude, longitude = map(float, location_input.split(","))
    user_location = (latitude, longitude)
    st.success(f"Your location: Latitude {latitude}, Longitude {longitude}")

    # Display map with user's location
    st.header("Your Location on the Map")
    m = folium.Map(location=user_location, zoom_start=15)

    # Add user location marker
    folium.Marker(user_location, popup="You are here", icon=folium.Icon(color="blue")).add_to(m)

    # Add billboard locations to the map
    for name, location in billboard_locations.items():
        folium.Marker(location, popup=name, icon=folium.Icon(color="red")).add_to(m)

    # Render the map
    st_folium(m, width=700, height=500)

    # Check proximity to billboards
    st.header("Proximity Check")
    found = False
    for name, location in billboard_locations.items():
        distance = ((latitude - location[0]) ** 2 + (longitude - location[1]) ** 2) ** 0.5
        if distance < 0.01:  # Example threshold for proximity
            found = True
            st.success(f"You are near {name}! Proceed to scan the billboard.")
            break

    if not found:
        st.error("You are not near any billboard. Move closer.")
else:
    st.info("Click 'Get My Location' to allow the app to retrieve your location.")
