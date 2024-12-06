import toml
import uuid

# Define the path for the TOML file
data_file = 'image_data.toml'

# Function to add image data to the TOML file
def add_image_data(image_url, location):
    # Generate a unique ID for the image
    image_id = str(uuid.uuid4())
    
    # Load existing data or create a new structure
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = toml.load(f)
    else:
        data = {"images": []}
    
    # Append new image data
    data["images"].append({
        "id": image_id,
        "location": location,
        "url": image_url
    })
    
    # Save data back to the TOML file
    with open(data_file, 'w') as f:
        toml.dump(data, f)
    print(f"Image data added with ID {image_id}")

# Example usage: Add a new image entry
image_url = "https://example.com/path/to/image1.jpg"
location = "35.6892, 51.3890"  # Example coordinates (Tehran)

add_image_data(image_url, location)
