import fitz
import os



# Define a function to convert PDF to images
def pdf_to_Img(foldername, location):
    image_folder = foldername
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # Open the PDF file
    try:
        doc = fitz.open(location)

    except Exception as e:
        return

    # Iterate over each page
    for page_num in range(len(doc)):
        page = doc[page_num]

        zoom_matrix = fitz.Matrix(4, 4)  # 4x4 matrix, scales up by 3 in both x and y directions
        # Render the page to an image
        try:
            image = page.get_pixmap(matrix=zoom_matrix)
           
        except Exception as e:
         
            continue

        # Save the image to a file in the image folder
        try:
            image.save(os.path.join(image_folder, f'page_{page_num+2}.png'))
            
        except Exception as e:
         
            continue

    doc.close()
    print("Done")
    
image_folder = 'images'
output_folder='pdf/pdf2.pdf'
pdf_to_Img(image_folder, output_folder)