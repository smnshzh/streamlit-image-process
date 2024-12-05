import streamlit as st
from PIL import Image
import cv2
import numpy as np
from ultralytics import YOLO  # Assuming YOLOv8 is installed via ultralytics

# Load the YOLO model
model = YOLO('yolov8s.pt')  # Replace with your YOLO weights file if needed

# Streamlit app
st.title("Object Detection with YOLO")

st.sidebar.title("Upload Image")
image_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if image_file:
    # Display the uploaded image
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert image to OpenCV format
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Perform object detection
    st.write("Running YOLO detection...")
    results = model(image_bgr)

    # Parse results
    annotated_frame = results[0].plot()  # Annotated image
    detections = results[0].boxes.data.numpy()  # YOLOv8 boxes

    # Count objects
    object_counts = {}
    for detection in detections:
        class_id = int(detection[5])  # Class index
        class_name = model.names[class_id]  # Get class name
        if class_name in object_counts:
            object_counts[class_name] += 1
        else:
            object_counts[class_name] = 1

    # Display results
    st.image(annotated_frame, caption="Detected Objects", use_column_width=True)

    st.write("### Object Count")
    for obj, count in object_counts.items():
        st.write(f"- **{obj}**: {count}")
else:
    st.write("Please upload an image to start detection.")
