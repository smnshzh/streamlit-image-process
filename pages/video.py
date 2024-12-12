import streamlit as st

# Title of the app
st.title("Video Player")

# Input for the video URL
video_url = st.text_input("Enter a video URL:")

if video_url:
    # Display the video
    st.video(video_url)
