import os
from PIL import Image

# Directories
input_image_dir = '*path*'    # Directory containing images
input_txt_dir = '*path*'     # Directory containing txt files
output_dir = '*path*'     # Directory to save cropped images

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def crop_image(image_path, coords):
    """
    Crop the image at the given path using the coordinates and return the cropped image.
    coords should be a tuple (x_center, y_center, width, height)
    """
    with Image.open(image_path) as img:
        img_width, img_height = img.size
        
        x_center, y_center, width, height = coords
        # Convert normalized coordinates to absolute pixel values
        x_center = x_center * img_width
        y_center = y_center * img_height
        width = width * img_width
        height = height * img_height

        x_min = x_center - width / 2
        y_min = y_center - height / 2
        x_max = x_center + width / 2
        y_max = y_center + height / 2

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

def process_images(image_dir, txt_dir, output_dir):
    """
    Process each image in the image directory, read its corresponding txt file for coordinates,
    crop the image, and save the cropped images to the output directory.
    """
    for image_name in os.listdir(image_dir):
        if image_name.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            image_path = os.path.join(image_dir, image_name)
            txt_filename = f"{os.path.splitext(image_name)[0]}.txt"
            txt_path = os.path.join(txt_dir, txt_filename)

            if os.path.exists(txt_path):
                print(f"Processing image: {image_name}")
                with open(txt_path, 'r') as f:
                    crop_index = 0
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) == 5:
                            _, x_center, y_center, width, height = map(float, parts)
                            coords = (x_center, y_center, width, height)
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
                            print(f"Invalid line in {txt_path}: {line}")
            else:
                print(f"No coordinates file found for image: {image_name}")

# Run the process
process_images(input_image_dir, input_txt_dir, output_dir)
