import cv2
import numpy as np

# Step 1: Load the image
image_path = 'images/page_1.png'  # Change this to your image path
image = cv2.imread(image_path)

# Step 2: Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 3: Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(gray, 255, 
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                               cv2.THRESH_BINARY_INV, 
                               11, 2)

# Step 4: Apply morphological operations to close gaps
kernel = np.ones((10, 10), np.uint8)
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=5)

# Step 5: Find contours
contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Step 6: Draw bounding boxes around each contour
for contour in contours:
    area = cv2.contourArea(contour)
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w)/h
    # Filter contours based on area and aspect ratio (change the thresholds as needed)
    if area > 10000 and 0.5 < aspect_ratio < 5:  # Adjust these values based on your image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color, thickness 2

# Step 7: Resize the image for display
width = 800  # Desired width
height = int(image.shape[0] * (width / image.shape[1]))  # Maintain aspect ratio
resized_image = cv2.resize(image, (width, height))

# Step 8: Display the result
cv2.imshow('Bounding Boxes', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()