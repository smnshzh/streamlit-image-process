import streamlit as st

# Title of the app
st.title("Video Downloader and Player")

# File uploader for video files
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save the uploaded video to a temporary file
    with open("uploaded_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display the uploaded video
    st.subheader("Uploaded Video:")
    st.video("uploaded_video.mp4")
