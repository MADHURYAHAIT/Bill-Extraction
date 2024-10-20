import os

import numpy as np
import google.generativeai as genai


from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def input_image_setup(file_location, type='image/png'):
    if file_location:
        with open(file_location, 'rb') as f:
                bytes_data = f.read()
        print("Data Extraction Started..")
        image_parts = [
                {
                    "mime_type": type,  
                    "data": bytes_data
                }
            ]

        input_prompt="""
                You are an expert in scanned images of invoices. There would be more than once invoice in the provided image. 
                Your job is to identify the number of invoices. create a bounding box around the invoice such once bounding box consists of one invoice and get the the coordinates of the bounding box if 
                the full canvas coordinates are left = 0 , top = 0 , right= 2448, bottom=3168. 
                The coordinates of the each of the invoices are needed so that they can be cropped as individual invoices.
                
                Format should not be changed anyhow.
                The identified invoices are = number
                Invoice 1
                [left coordinate, top coordinate, right coordinate, bottom coordinate]
                Invoice 2
                [left coordinate, top coordinate, right coordinate, bottom coordinate]
                so on...
            """

        generation_config = {
            "temperature": 0.1,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
            }
        model=genai.GenerativeModel('gemini-1.5-flash',generation_config=generation_config)
        response=model.generate_content([input_prompt,image_parts[0]])
        # print(response.text)
        print("Data Extracted Successfully!")
        return response.text



def process(list_a):
    print("Data Processing...")
    Data=[]
    columns=[]
    columns.append(list_a[0][1:4])
    for i in range(1,len(list_a)):
        Data.append(list_a[i][1:4])
    d = np.array(Data)
    return d,columns



if __name__ == "__main__":
    # if len(sys.argv)!= 2:
    #     print("Usage: python script.py <file_location>")
    #     sys.exit(1)
    file_location = "images\page_1.png"
    Raw=input_image_setup(file_location)
    print(Raw)
    # Raw = Raw.replace("\t", "").replace(" ", "")
    # list_a = ast.literal_eval(Raw)
    # d,c = process(list_a)
    # data_to_xlsx(d, c[0], "output/output.xlsx")
    print("Script Success !")