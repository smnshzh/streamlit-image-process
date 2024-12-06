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
phone_number = st.text_input("Phone Number")

if st.button("Submit Information"):
    # Check if input is numeric and has the correct length
    if not name or not phone_number:
        st.error("Please enter both your name and phone number.")
    elif not phone_number.isdigit():
        st.error("Phone number must only contain digits.")
    elif len(phone_number) != 11:
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

# Step 2: Display map for location recognition
st.header("Step 2: Identify the Location")

# Create a map centered at an initial location
m = folium.Map(location=[35.6892, 51.3890], zoom_start=15)

# Add a click event for getting the latitude and longitude
click_marker = folium.LatLngPopup()
m.add_child(click_marker)

# Display the map
st_folium(m, width=700, height=500)

# Get latitude and longitude from user interaction
st.write("Select your location on the map by clicking.")
lat, lon = st.session_state.get('lat'), st.session_state.get('lon')

if lat is not None and lon is not None:
    st.write(f"Selected Location: Latitude {lat}, Longitude {lon}")

    # Step 3: Button to save location
    if st.button("Save Location"):
        # Save the user's location to the TOML file
        user_data = {
            "user": {
                "name": name,
                "phone_number": phone_number,
                "latitude": lat,
                "longitude": lon
            }
        }
        with open(data_file, 'w') as f:
            toml.dump(user_data, f)
        st.success("Location has been saved successfully!")
