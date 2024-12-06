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
    function getLocation() {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const long = position.coords.longitude;
                const location = `${lat},${long}`;
                const locationInput = document.getElementById("geo");
                locationInput.value = location;
                locationInput.dispatchEvent(new Event('change'));
            },
            (error) => {
                alert('Unable to access your location. Please enable location services and reload the page.');
            }
        );
    }
    getLocation();
    </script>
    """

# App Title
st.title("Treasure Hunt App")

# Step 1: Get User Location Automatically
st.header("Step 1: Automatic Location Detection")
st.write("The app is detecting your location. Please allow access to your location in the browser settings.")

js_code = get_js_for_gps()
st.markdown(js_code, unsafe_allow_html=True)

# Hidden text input to receive JavaScript's location data
location_input = st.text_input("Hidden Location", key="geo", label_visibility="hidden")

if location_input:
    latitude, longitude = map(float, location_input.split(","))
    user_location = (latitude, longitude)
    st.success(f"Location detected: {user_location}")

    # Display the map with user's location
    st.header("Your Location on the Map")
    m = folium.Map(location=user_location, zoom_start=15)

    # Add user location marker to the map
    folium.Marker(user_location, popup="You are here", icon=folium.Icon(color="blue")).add_to(m)

    # Add billboard locations to the map
    for name, location in billboard_locations.items():
        folium.Marker(location, popup=name, icon=folium.Icon(color="red")).add_to(m)

    # Render the map in the app
    st_folium(m, width=700, height=500)

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

    # Invitation to the event after completing all scans
    st.header("Final Step: Receive Your Invitation")
    if st.button("Complete the Treasure Hunt"):
        st.balloons()
        st.success("Congratulations! You are invited to the grand event. Check your email for details.")
else:
    st.error("Location not detected. Please enable location services in your browser and reload the page.")
