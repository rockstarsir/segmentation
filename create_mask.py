import json
import numpy as np
from PIL import Image, ImageDraw
import sys

# Function to create a multi-class colored mask
def create_colored_mask(json_data, image_size, category_color_mapping):
    # Create an empty RGB image for the mask, initialized with black (0, 0, 0)
    mask = Image.new('RGB', image_size, (0, 0, 0))
    draw = ImageDraw.Draw(mask)

    for image_info in json_data:
        labels = image_info['labels']

        for label in labels:
            category = label['category']
            
            # If the category is in the mapping, use the associated color for that category
            if category in category_color_mapping:
                category_color = category_color_mapping[category]
                
                for poly in label['poly2d']:
                    vertices = [(x, y) for x, y in poly['vertices']]
                    # Draw the polygon with the assigned color for the category
                    draw.polygon(vertices, outline=category_color, fill=category_color)
    
    return mask

# Check for command line arguments to get the JSON file path
# if len(sys.argv) < 2:
#     print("Usage: python create_masks.py <path_to_json_file>")
#     sys.exit(1)

# Load the JSON d"ata from the specified file path
json_file_path = "/home/drv/work_drv/YOLOP-main/mask/sem_seg_val.json"
try:
    with open(json_file_path, 'r') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error reading the JSON file: {e}")
    sys.exit(1)

# Define the image size (you may need to adjust this based on your image dimensions)
image_size = (1024, 1024)  # Example size; replace with your actual size

# Define a mapping from category names to unique RGB colors
category_color_mapping = {
    'car': (255, 0, 0),       # Red
    'person': (0, 255, 0),    # Green
    'bicycle': (0, 0, 255),   # Blue
    'truck': (255, 255, 0),   # Yellow
    'motorcycle': (255, 0, 255), # Magenta
    'bus': (0, 255, 255),     # Cyan
    'traffic_light': (128, 0, 128), # Purple
    'stop_sign': (255, 165, 0) # Orange
}

# Get the total number of images to be processed
total_images = len(data)
print(f"Total images to process: {total_images}")

# Loop through the images and create a multi-class colored mask for each
for image_info in data:
    image_name = image_info['name']
    print(f"Creating multi-class colored mask for {image_name}...")
    
    # Create the multi-class colored mask for this image
    mask_image = create_colored_mask([image_info], image_size, category_color_mapping)
    
    # Save the mask image (same name as the original image but with "_colored_mask" suffix)
    mask_image.save(f"{image_name.split('.')[0]}_colored_mask.png")

print("Multi-class colored mask creation complete.")
