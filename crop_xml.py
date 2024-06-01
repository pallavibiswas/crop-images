import os
import xml.etree.ElementTree as ET
from PIL import Image

# Directories
input_image_dir = '*path*'
input_xml_dir = '*path*'
output_dir = '*path*'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def crop_image(image_path, coords):
    """
    Crop the image at the given path using the coordinates and return the cropped image.
    coords should be a tuple (x_min, y_min, x_max, y_max)
    """
    with Image.open(image_path) as img:
        img_width, img_height = img.size
        x_min, y_min, x_max, y_max = coords

        # Print debug information
        print(f"Original Image Size: {img.size}")
        print(f"Requested Crop Box: ({x_min}, {y_min}, {x_max}, {y_max})")

        # Ensure the crop box is within image bounds
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(img_width, x_max)
        y_max = min(img_height, y_max)

        # Print adjusted crop box
        print(f"Adjusted Crop Box: ({x_min}, {y_min}, {x_max}, {y_max})")

        # If the crop box is invalid (e.g., x_max <= x_min or y_max <= y_min), return the original image
        if x_min >= x_max or y_min >= y_max:
            print("Invalid crop box; returning the original image.")
            return img

        cropped_img = img.crop((x_min, y_min, x_max, y_max))
        return cropped_img

def process_images(image_dir, xml_dir, output_dir):
    """
    Process each image in the image directory, read its corresponding xml file for coordinates,
    crop the image, and save the cropped images to the output directory.
    """
    for image_name in os.listdir(image_dir):
        if image_name.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            image_path = os.path.join(image_dir, image_name)
            xml_filename = f"{os.path.splitext(image_name)[0]}.xml"
            xml_path = os.path.join(xml_dir, xml_filename)

            if os.path.exists(xml_path):
                print(f"Processing image: {image_name}")
                tree = ET.parse(xml_path)
                root = tree.getroot()
                crop_index = 0
                for obj in root.findall('.//bndbox'):
                    x_min = int(obj.find('xmin').text)
                    y_min = int(obj.find('ymin').text)
                    x_max = int(obj.find('xmax').text)
                    y_max = int(obj.find('ymax').text)
                    coords = (x_min, y_min, x_max, y_max)
                    try:
                        cropped_img = crop_image(image_path, coords)
                        output_image_name = f"{os.path.splitext(image_name)[0]}_crop{crop_index}{os.path.splitext(image_name)[1]}"
                        output_image_path = os.path.join(output_dir, output_image_name)
                        cropped_img.save(output_image_path)
                        print(f"Cropped image saved to: {output_image_path}")
                        crop_index += 1
                    except Exception as e:
                        print(f"Error processing {image_name} with coordinates {coords}. Error: {e}")
            else:
                print(f"No coordinates file found for image: {image_name}")

# Run the process
process_images(input_image_dir, input_xml_dir, output_dir)