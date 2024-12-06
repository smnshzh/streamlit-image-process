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

# App Title
st.title("Treasure Hunt App")

# Step 1: Get User Location
st.header("Step 1: Share Your Location")

latitude = st.number_input("Enter your latitude", format="%.6f")
longitude = st.number_input("Enter your longitude", format="%.6f")

user_location = (latitude, longitude)

if latitude and longitude:
    st.write(f"Your location: {user_location}")

    # Step 2: Check Proximity to Billboards
    st.header("Step 2: Find Nearby Billboards")

    found = False
    for name, location in billboard_locations.items():
        if is_near_location(user_location, location):
            found = True
            st.success(f"You're near {name}! Proceed to scan the billboard.")

            # Step 3: Simulate Scanning
            st.header("Step 3: Scan the Billboard")
            uploaded_file = st.file_uploader("Upload a photo of the billboard")

            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                st.success("Billboard scanned successfully! Proceed to the next step.")
                break

    if not found:
        st.error("You are not near any billboards. Move closer to continue.")

    # Map visualization
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
if st.button("Complete the Treasure Hunt"):
    st.balloons()
    st.success("Congratulations! You are invited to the grand event. Check your email for details.")
