# import streamlit as st
# import pdfplumber
# import matplotlib.pyplot as plt

# # Upload PDF file
# st.title("Interactive PDF Word Position Extractor")
# uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# if uploaded_file:
#     with pdfplumber.open(uploaded_file) as pdf:
#         page = pdf.pages[0]  # Extract first page
#         words = page.extract_words()  # Extract words with positions
#         img = page.to_image()

#         # Display image
#         fig, ax = plt.subplots(figsize=(10, 12))
#         ax.imshow(img.annotated)
#         ax.axis("off")
#         st.pyplot(fig)

#         # User selects a word
#         selected_word = st.selectbox("Select a word to get position", [w["text"] for w in words])

#         # Find the selected word's position
#         for word in words:
#             if word["text"] == selected_word:
#                 st.write(f"**Word:** {word['text']}")
#                 st.write(f"**x0 (Left):** {word['x0']}")
#                 st.write(f"**x1 (Right):** {word['x1']}")
#                 st.write(f"**Top:** {word['top']}")
#                 st.write(f"**Bottom:** {word['bottom']}")
#                 break


# import streamlit as st
# import pdfplumber
# import numpy as np
# import cv2
# from PIL import Image
# from streamlit_drawable_canvas import st_canvas
# import gc
# gc.collect()
# # Title
# st.title("📄 Interactive PDF Word Extractor")

# # Upload PDF
# uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# if uploaded_file:
#     with pdfplumber.open(uploaded_file) as pdf:
#         page = pdf.pages[0]  # First page
#         words = page.extract_words()  # Extract words with positions

#         # Convert PDF to image
#         img = page.to_image()
#         img_cv = np.array(img.original)

#         # Draw word bounding boxes
#         for word in words:
#             x0, top, x1, bottom = int(word["x0"]), int(word["top"]), int(word["x1"]), int(word["bottom"])
#             cv2.rectangle(img_cv, (x0, top), (x1, bottom), (255, 0, 0), 2)

#         # Display image with annotation area
#         img_pil = Image.fromarray(img_cv)
#         st.image(img_pil, caption="Draw a box around the words to extract", use_column_width=True)

#         # Create an interactive canvas
#         canvas = st_canvas(
#             fill_color="rgba(255, 0, 0, 0.3)", 
#             stroke_width=3, 
#             stroke_color="red",
#             background_image=img_pil, 
#             height=img_cv.shape[0],
#             width=img_cv.shape[1],
#             drawing_mode="rect",
#             key="canvas"
#         )

#         # Extract words from selected area
#         if canvas.json_data:
#             objects = canvas.json_data["objects"]
#             if objects:
#                 obj = objects[0]  # Get the first drawn rectangle
#                 x0, y0 = obj["left"], obj["top"]
#                 x1, y1 = x0 + obj["width"], y0 + obj["height"]

#                 # Find words inside the drawn box
#                 extracted_words = [
#                     w["text"] for w in words
#                     if x0 <= w["x0"] <= x1 and y0 <= w["top"] <= y1
#                 ]

#                 if extracted_words:
#                     st.success(f"Extracted Words: {' '.join(extracted_words)}")
#                 else:
#                     st.warning("No words found in the selected area!")

# import streamlit as st
# import pdfplumber
# import json
# import os

# TEMPLATE_FILE = "invoice_template.json"

# # Function to extract words safely
# def extract_pdf_text(pdf_path):
#     with pdfplumber.open(pdf_path) as pdf:
#         page = pdf.pages[0]
#         words = page.extract_words()
        
#         # Normalize keys to avoid KeyError
#         extracted = []
#         for word in words:
#             extracted.append({
#                 "text": word["text"],
#                 "x0": word.get("x0", 0),  # Use default values if key is missing
#                 "x1": word.get("x1", 0),
#                 "y0": word.get("top", 0),  # Use 'top' instead of 'y0'
#                 "y1": word.get("bottom", 0)  # Use 'bottom' instead of 'y1'
#             })
        
#         return extracted

# # Function to save template
# def save_template(template):
#     with open(TEMPLATE_FILE, "w") as f:
#         json.dump(template, f, indent=4)
#     st.success("Template saved successfully!")

# # Function to load template
# def load_template():
#     if os.path.exists(TEMPLATE_FILE):
#         with open(TEMPLATE_FILE, "r") as f:
#             return json.load(f)
#     return {}

# st.title("Invoice Template Creator")

# # File Upload
# uploaded_file = st.file_uploader("Upload an Invoice PDF", type=["pdf"])
# if uploaded_file:
#     with open("temp_invoice.pdf", "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     words = extract_pdf_text("temp_invoice.pdf")
    
#     st.subheader("Extracted Text")
#     for word in words:
#         st.write(f"**{word['text']}** - (x0={word['x0']}, y0={word['y0']})")

#     # Create template fields
#     st.subheader("Define Template")
#     invoice_no = st.text_input("Invoice No (Extracted Text)")
#     invoice_date = st.text_input("Invoice Date (Extracted Text)")
#     total_amount = st.text_input("Total Amount (Extracted Text)")

#     if st.button("Save Template"):
#         template = {
#             "invoice_no": invoice_no,
#             "invoice_date": invoice_date,
#             "total_amount": total_amount
#         }
#         save_template(template)

# # Load & display template
# if st.button("Load Saved Template"):
#     template = load_template()
#     if template:
#         st.json(template)
#     else:
#         st.warning("No template found!")
# s

import streamlit as st
import pdfplumber
import re
import pandas as pd

# Function to extract floats
def extract_floats(text):
    float_pattern = r'\b\d+\.\d+\b'
    return re.findall(float_pattern, text)

# Function to extract all words and their coordinates from the PDF
def extract_words_and_coordinates(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[2]
        words = first_page.extract_words()

        word_coords = {}
        for word in words:
            word_coords[word['text']] = {
                'x0': word['x0'],
                'top': word['top'],
                'bottom': word['bottom'],
                'x1': word['x1']
            }

        return word_coords

# Streamlit Interface
st.title("PDF Table Extraction")
pdf_path = st.file_uploader("Upload a PDF", type="pdf")

if pdf_path is not None:
    # Extract all words and their coordinates
    word_coords = extract_words_and_coordinates(pdf_path)
    
    # Get a list of unique words (ignoring case and duplicates)
    unique_words = list(set(word_coords.keys()))
    
    # Dropdown for selecting words dynamically
    selected_word1 = st.selectbox('Select first word for coordinate extraction', options=unique_words)
    selected_word2 = st.selectbox('Select second word for coordinate extraction', options=unique_words)
    selected_word3 = st.selectbox('Select third word for coordinate extraction', options=unique_words)
    
    # Display selected words and their coordinates
    st.write(f"Selected first word: {selected_word1} with coordinates {word_coords[selected_word1]}")
    st.write(f"Selected second word: {selected_word2} with coordinates {word_coords[selected_word2]}")
    st.write(f"Selected third word: {selected_word3} with coordinates {word_coords[selected_word3]}")
    
    # Extract and display table from the selected coordinates
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[2]
        
        # Get the coordinates of the selected words
        x0, top = word_coords[selected_word1]['x0'], word_coords[selected_word1]['top']
        x1 = word_coords[selected_word3]['x1']
        bottom = word_coords[selected_word2]['bottom']
        
        # Crop the page based on selected coordinates
        box = (x0, top, x1, bottom)
        page = first_page.crop(bbox=box)
        table = page.extract_table(table_settings={
            "vertical_strategy": "text",
            "horizontal_strategy": "text",
        })
        
        if table:
            df = pd.DataFrame(table[1:])
            st.write(df)
        
        
        # Extract text and find floats
        text = page.extract_text()
        text = text.replace(",", "")
        sx = text.split('\n')
        for ml in sx:
            floats = extract_floats(ml)  # Extract floats from the text
            if not floats:
                st.write(f"Floats found: {ml}")
      


# Open the PDF


