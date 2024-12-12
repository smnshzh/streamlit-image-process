import streamlit as st
import requests

# Title of the app
st.title("Video Downloader and Player")

# Input for the video URL
video_url = st.text_input("Enter a video URL:")

if video_url:
    try:
        # Download the video
        response = requests.get(video_url)
        response.raise_for_status()  # Check for errors

        # Save the video to a temporary file
        with open("downloaded_video.mp4", "wb") as f:
            f.write(response.content)

        # Display the downloaded video
        st.subheader("Downloaded Video:")
        st.video("downloaded_video.mp4")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
