import streamlit as st
from streamlit_folium import st_folium
import folium
import toml
import os

# Define the file path for saving data
data_file = 'user_data.toml'

# Check if the file exists; if not, create it with an initial structure
if not os.path.exists(data_file):
    initial_data = {
        "user": {
            "name": "",
            "phone_number": "",
            "latitude": None,
            "longitude": None
        }
    }
    with open(data_file, 'w') as f:
        toml.dump(initial_data, f)

# Title
st.title("Treasure Hunt App")

# Step 1: Collect user information
st.header("Step 1: Enter Your Information")
name = st.text_input("Name")
phone_number = st.text_input("Phone Number", type="number")

if st.button("Submit Information"):
    if not name or not phone_number:
        st.error("Please enter both your name and phone number.")
    elif len(str(phone_number)) != 11:
        st.error("Phone number must be exactly 11 characters long.")
    else:
        # Save the user's information to a TOML file
        user_data = {
            "user": {
                "name": name,
                "phone_number": phone_number
            }
        }
        with open(data_file, 'w') as f:
            toml.dump(user_data, f)
        st.success("Your information has been saved successfully!")

# Step 2: Display an image for location recognition
st.header("Step 2: Identify the Location")
st.image("example_image.jpg", caption="Example Image", use_column_width=True)

# Initialize map
default_location = (35.6892, 51.3890)  # Example coordinates (Tehran)
m = folium.Map(location=default_location, zoom_start=12)

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

# Step 3: Capture the user's selection and save it
if map_data and "last_clicked" in map_data:
    user_location = map_data["last_clicked"]
    latitude, longitude = user_location["lat"], user_location["lng"]
    st.success(f"Your selected location: Latitude {latitude}, Longitude {longitude}")

    # Save the location data to the TOML file
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = toml.load(f)
        data["user"]["latitude"] = latitude
        data["user"]["longitude"] = longitude

        with open(data_file, 'w') as f:
            toml.dump(data, f)
        st.success("Your location has been saved successfully!")
else:
    st.warning("Drag the blue marker to your location and click on the map to confirm.")
