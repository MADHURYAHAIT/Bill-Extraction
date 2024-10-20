import cv2
import pytesseract
import numpy as np

# Specify Tesseract OCR executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

def extract_invoice_coordinates(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return []

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Number of contours found: {len(contours)}")

    # Filter and process contours to identify actual invoice regions
    invoice_coordinates = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h

        # Adjust filtering criteria
        if area > 1000 and 0.3 < aspect_ratio < 3:  # More lenient filtering
            # Extract the region of interest for OCR text density check
            roi = gray[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi, config='--oem 3 --psm 6')
            if len(text.strip()) > 5:  # Ensure the ROI contains some meaningful text
                invoice_coordinates.append([x, y, x + w, y + h])
                print(f"Detected Invoice: [ {x}, {y}, {x + w}, {y + h} ]")  # Debugging output

    # Draw bounding boxes around detected invoices
    for coord in invoice_coordinates:
        cv2.rectangle(image, (coord[0], coord[1]), (coord[2], coord[3]), (0, 255, 0), 2)  # Green box for invoices

    # Resize image for display
    height, width = image.shape[:2]
    scale = 800 / width  # Scale to a width of 800 pixels
    new_dimensions = (800, int(height * scale))
    resized_image = cv2.resize(image, new_dimensions)

    # Display the image with detected invoices
    cv2.imshow("Detected Invoices", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return invoice_coordinates

# Example usage
image_path = "images/page_1.png"
coordinates = extract_invoice_coordinates(image_path)

print("Invoice Coordinates:")
for coord in coordinates:
    print(f"[ {coord[0]}, {coord[1]}, {coord[2]}, {coord[3]} ]")
