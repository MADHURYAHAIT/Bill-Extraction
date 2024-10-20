from PIL import Image

# Function to crop an image from a given image file
def crop_image_from_file(image_path, crop_box, output_png_path):
    # Open the image
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Crop the image using the specified crop_box (left, top, right, bottom)
    cropped_image = image.crop(crop_box)

    # Save the cropped image as a PNG
    cropped_image.save(output_png_path, format="PNG")
    print(f"Saved cropped image to {output_png_path}")

# Usage
image_path = "images\page_2.png"  # Specify your input image file here
crop_box = (0, 0, 1248, 800)  # Coordinates for cropping 
#(left, top, right, bottom)
output_png_path = "cropped_image.png"  # Output PNG file name

crop_image_from_file(image_path, crop_box, output_png_path)