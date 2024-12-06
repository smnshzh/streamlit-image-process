import streamlit as st
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

# Predefined billboard locations (latitude, longitude)
billboard_locations = {
    "Billboard 1": (35.6892, 51.3890),  # Example coordinates (Tehran)
    "Billboard 2": (35.7156, 51.4027),  # Example coordinates (Tehran)
}

# Function to check if user is near a billboard
def is_near_location(user_location, target_location, radius=0.5):
    distance = geodesic(user_location, target_location).km
    return distance <= radius

# Function to load JavaScript for GPS
def get_js_for_gps():
    return """
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const long = position.coords.longitude;
            document.getElementById("geo").value = `${lat},${long}`;
        },
        (error) => {
            alert('Unable to access your location. Please enable location services and reload the page.');
        }
    );
    </script>
    """

# App Title
st.title("Treasure Hunt App")

# Step 1: Get User Location Automatically
st.header("Step 1: Automatic Location Detection")
st.write("Allow your browser to access your location. If location services are disabled, enable them and reload the page.")

js_code = get_js_for_gps()
st.markdown(js_code, unsafe_allow_html=True)
location_input = st.text_input("Your current location (auto-filled)", key="geo")

# Validate location input
if not location_input:
    st.error("Location not detected. Please enable location services and reload the page.")
else:
    latitude, longitude = map(float, location_input.split(","))
    user_location = (latitude, longitude)
    st.success(f"Location detected: {user_location}")

    # Step 2: Check Proximity to Billboards
    st.header("Step 2: Check Proximity")
    found = False
    for name, location in billboard_locations.items():
        if is_near_location(user_location, location):
            found = True
            st.success(f"You're near {name}! Proceed to scan the billboard.")

            # Step 3: Upload Image
            st.header("Step 3: Scan the Billboard")
            uploaded_file = st.file_uploader("Upload a photo of the billboard")
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

                # Simulate Image Validation
                if "valid_image_condition":  # Replace with actual image validation
                    st.success(f"Billboard {name} scanned successfully! Proceed to the next task.")
                else:
                    st.error("The uploaded image is incorrect. Please try again.")
            break

    if not found:
        st.error("You are not near any billboards. Move closer to continue.")

    # Map Visualization
    st.header("Map View")
    map_center = user_location
    m = folium.Map(location=map_center, zoom_start=15)

    # Add user location to map
    folium.Marker(user_location, popup="You are here", icon=folium.Icon(color="blue")).add_to(m)

    # Add billboard locations to map
    for name, location in billboard_locations.items():
        folium.Marker(location, popup=name, icon=folium.Icon(color="red")).add_to(m)

    st_folium(m, width=700, height=500)

# Invitation to the event after completing all scans
st.header("Final Step: Receive Your Invitation")
if location_input and st.button("Complete the Treasure Hunt"):
    st.balloons()
    st.success("Congratulations! You are invited to the grand event. Check your email for details.")
