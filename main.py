import fitz  # PyMuPDF
from PIL import Image
import io

# Function to extract and crop an image from a PDF
def crop_image_from_pdf(pdf_path, page_num, crop_box, output_png_path):
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Select the desired page
    page = pdf_document.load_page(page_num)

    # Extract the image list from the page
    image_list = page.get_images(full=True)

    if len(image_list) == 0:
        print("No images found on this page!")
        return

    # Get the first image on the page (or adjust as needed)
    img_index = image_list[0][0]
    base_image = pdf_document.extract_image(img_index)
    image_bytes = base_image["image"]
    
    # Convert the image into a PIL Image object
    image = Image.open(io.BytesIO(image_bytes))

    # Crop the image using the specified crop_box (left, top, right, bottom)
    cropped_image = image.crop(crop_box)

    # Save the cropped image as a PNG
    cropped_image.save(output_png_path, format="PNG")
    print(f"Saved cropped image to {output_png_path}")

# Usage
pdf_path = "pdf/first.pdf"  # Specify your PDF file here
page_num = 0          # Page number to extract the image from (0-based index)
crop_box = (0, 0, 1096, 4674)  # Coordinates for cropping (left, top, right, bottom)
output_png_path = "cropped_image.png"  # Output PNG file name

crop_image_from_pdf(pdf_path, page_num, crop_box, output_png_path)
