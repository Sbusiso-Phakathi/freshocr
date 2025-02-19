# import streamlit as st
# import pdfplumber
# import re
# import pandas as pd
# # Function to extract text from PDF and get unique words
# def extract_words_from_pdf(pdf_file):
#     with pdfplumber.open(pdf_file) as pdf:
#         text = ''
#         for page in pdf.pages:
#             text += page.extract_text()
        
#         # Extract unique words
#         words = set(re.findall(r'\w+', text.lower()))  # Normalize to lowercase
#         return sorted(words)

# # Streamlit UI
# st.title("PDF Word Selection for Regex")

# # File uploader
# pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
# comp = "adbc"


    
#     # Display words in a multi-select box
   

# with pdfplumber.open(pdf_file) as pdf:

#     if pdf_file:
#     # Extract words from PDF
#         words = extract_words_from_pdf(pdf_file)
    
#     # Display words in a multi-select box
#     start = st.text_input("Select start for regex", words)
#     end = st.text_input("Select end for regex", words)

    
#     pages = pdf.pages
#     for page in pdf.pages:
#         text = page.extract_text()
#         for line in text.split('\n'):

#             if comp == "abc":
#                 pattern = re.compile(rf'{re.escape(start)}\s*\n(.*?)\n\s*{re.escape(end)}', re.DOTALL | re.IGNORECASE)
#                 match = pattern.search(text)

#                 if match:
#                     extracted_text = match.group(1).strip()
                    
#                     # Convert extracted text into a list of lines
#                     lines = extracted_text.split("\n")

#                     # List to store structured data
#                     data = []

#                     for line in lines:
#                         # Regex to match structured invoice line items (Stock Code present)
#                         item_pattern = re.compile(r'(\d+)\s+([A-Za-z0-9\s\-]+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)', re.IGNORECASE)

#                         match = re.match(r'(\S+)\s+(.+?)\s+(\d+\.\d+)\s+(\S+)\s+(\d+\.\d+)\s+(\d+\.\d+)', line)
#                         if match:
#                             stock_code, description, quantity, unit, rate, sub_total = match.groups()
#                             data.append([stock_code, description, quantity, unit, rate, sub_total])

#                         else:
#                             # Regex for charge items (flexible number detection)
#                             charge_match = re.match(r'(.+?)\s+(\d+\.\d+)\s+(\d+\.\d+)(?:\s+(\d+\.\d+))?', line)
#                             if charge_match:
#                                 description, num1, num2, num3 = charge_match.groups()
#                                 quantity = num1  # Assume first number is quantity
#                                 rate = num2       # Assume second number is rate
#                                 sub_total = num3 if num3 else None  # Handle optional subtotal
#                                 data.append([None, description, quantity, None, rate, sub_total])

#                             else:
#                                 # Handle unstructured lines (free text like "VLAKLAAGTE")
#                                 data.append([None, line, None, None, None, None])

#                     # Convert to DataFrame
#                     df = pd.DataFrame(data, columns=["Stock Code", "Description", "Quantity", "Unit", "Rate", "Sub-Total"])

#                     print(df)
#             else:


#                     pattern = re.compile(rf'{re.escape(start)}\s*(.*?)\s*{re.escape(end)}', re.DOTALL)

#                     match = pattern.search(text)
#                     if match:
#                         extracted_text = match.group(1).strip()

#                         # Regex to extract structured data (No., Description, Quantity, Unit, Unit Price, Total (Excl.), VAT, Total (Incl.))
#                         item_pattern = re.compile(r'(\d+)\s+([A-Za-z0-9\s\-]+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)', re.IGNORECASE)

#                         data = []
                        
#                         # Find all matches for the structured data
#                         for line in extracted_text.split("\n"):
#                             match = item_pattern.match(line)
#                             if match:
#                                 no, description, quantity, unit_price, total_excl, vat = match.groups(1)
#                                 data.append([no, description.strip(), quantity, unit_price, total_excl, vat])

#                         # Create a DataFrame
#                         df = pd.DataFrame(data, columns=["No.", "Description", "Quantity", "Unit Price", "Total (Excl.)", "VAT"])

#                         print(df)

# import streamlit as st
# import pdfplumber
# import re
# import pandas as pd

# # Function to extract text from PDF and get unique words
# def extract_words_from_pdf(pdf_file):
#     with pdfplumber.open(pdf_file) as pdf:
#         text = ''.join(page.extract_text() for page in pdf.pages)
        
#         # Extract unique words
#         words = set(re.findall(r'\w+', text.lower()))  # Normalize to lowercase
#         return sorted(words)

# # Function to extract structured data from text
# def BKB(text, start, end, comp):
#     pattern = re.compile(rf'{re.escape(start)}\s*\n(.*?)\n\s*{re.escape(end)}', re.DOTALL | re.IGNORECASE)
    
#     match = pattern.search(text)
#     if match:
#         extracted_text = match.group(1).strip()
        
#         # Regex patterns for structured data
#         item_pattern = re.compile(r'([A-Za-z0-9\s]+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)', re.IGNORECASE)
        
#         data = []
#         for line in extracted_text.split("\n"):
#             match = item_pattern.match(line)
#             if match:
#                 a,b,c,d  = match.groups()
#                 data.append([None, a, None, None, None, None,b, c, d])
#                 print (match.groups())
#             else:
#                 # Regex for charge items (flexible number detection)
#                 charge_match = re.match(r'(\S+)\s+(.+?)\s+(\d+\.\d+)\s+(\S+)\s+(\d+\.\d+)\s+(\d+\.\d+)', line)
#                 if charge_match:
#                     scode, description, num1, num2, num3, dsds,  = charge_match.groups()
#                     branch = re.search(r'Branch\s+(\S+)', text)
#                     silo =  branch.group(1)
#                     lld = description.split(" ")
#                     print(charge_match.groups())
#                     data.append([scode, description, lld[0], lld[2], num1, num3, dsds, None, None, silo if num3 else None])
#                 else:
#                     # Handle unstructured lines (free text)
#                     data.append([None, line, None, None, None, None])

#         return pd.DataFrame(data, columns=["Stock Code", "Description", "Crop", "Grade", "Quantity", "Rate", "Sub-Total", "VAT", "Total", "Cost Type"])
    
# def AFGRI(text, start, end, comp):
#     pattern = re.compile(rf'{re.escape(start)}\s*\n(.*?)\n\s*{re.escape(end)}', re.DOTALL | re.IGNORECASE)
    
#     match = pattern.search(text)
#     if match:
#         extracted_text = match.group(1).strip()
#         extracted_text = extracted_text.replace(",","")
#         print(extracted_text)
#         # Regex patterns for structured data
#         item_pattern = re.compile(r'(\d+)\s+([A-Za-z0-9\s\-]+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)', re.IGNORECASE)
        
#         data = []
#         for line in extracted_text.split("\n"):
#             match = item_pattern.match(line)
#             if match:
#                 a,b,c,d,e,f, g = match.groups()
#                 match2 = re.search(r'MBIC[:\s]*(\S+)', text)
#                 grade  =  match2.group(1)
#                 commodity = b.split(" ")[0:2]
#                 crop = b.split(" ")[-1:]
#                 match3 = re.search(r'(\S+)\s+Siloco', text)
#                 silo =  match3.group(1)
#                 data.append([b, c, d, e, f, g, grade, silo, crop, commodity])


#         return pd.DataFrame(data, columns=["Description", "Quantity","Unit Price", "Total (Excl.)", "VAT", "Total (Incl.)", "Grade", "Cost Type", "Crop", "Commodity"])

# # Streamlit UI
# st.title("PDF Word Selection for Regex")

# # File uploader
# pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# if pdf_file:
#     words = extract_words_from_pdf(pdf_file)
    
#     # Display words in a multi-select box
#     start = st.text_input("Select start for regex", words)
#     end = st.text_input("Select end for regex", words)
    
#     comp = "abc"  # Example, can be dynamic based on user input

#     # Process the PDF
#     with pdfplumber.open(pdf_file) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()
#             df = AFGRI(text, start, end, comp)
#             # st.dataframe(df)
#             st.write(df)



import streamlit as st
import pdfplumber
import re
import pandas as pd

# Function to extract text from a single PDF file
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    return text

# Function to extract structured data for AFGRI format
def extract_afgri_data(text, start, end):
    import re

    pattern = re.compile(rf'{re.escape(start)}\s*\n(.*?)\n\s*{re.escape(end)}', re.DOTALL | re.IGNORECASE)
    match = pattern.search(text)
    tt = text.split("\n")

    # col1, col2 = st.columns(2)
    # with col1:
    #     st.multiselect("select item: ", tt)
    # with col2:
    #     st.multiselect("select item: ", ["A","B","C"])


    # Initialize session state for number of rows




    import re, csv

    # Initialize session state for number of rows
    if "num_rows" not in st.session_state:
        st.session_state.num_rows = 1  # Start with 1 row

    # Define the list of attributes for Column 1
    tttt = ["A", "B", "C", "D"]

    # Define the list of attribute items for Column 2 (Example Data)

    st.write("### Dynamic Multi-Select Table")

    # Function to exclude words, find the next first word and extract text between exclusions
    def process_text(selected_text, next_text, row_index, text):
        words = selected_text.split(" ")  # Split text into words
        excluded_words = st.multiselect(f"Select words to exclude (Row {row_index+1}):", words, key=f"exclude_{row_index}_{selected_text}")

        if excluded_words:
            # Join the excluded words into a phrase
            excluded_phrase = " ".join(excluded_words)

            # Find the first word of the next attribute item
            next_first_word = next_text.split(" ")[0] if next_text else None

            # Regex to find everything between excluded phrase and next first word
            if next_first_word:
                pattern = rf"{re.escape(excluded_phrase)}\s+(.*?)\s+{re.escape(next_first_word)}"
                match = re.search(pattern, text)
                if match:
                    text_between = match.group(1)  # Extract text between the exclusions and the next word
                else:
                    text_between = "No text found between exclusions and next first word"
            else:
                text_between = "Next attribute not available"

            return excluded_phrase, text_between, next_first_word
        return None, None, None
    

    # Display existing rows
    for i in range(st.session_state.num_rows):
        col1, col2 = st.columns(2)

        with col1:
            attribute = st.multiselect(f"Attribute (Row {i+1}):", tttt, key=f"col1_{i}")

        with col2:
            selected_col2 = st.multiselect(f"Select Attribute Item (Row {i+1}):", tt, key=f"col2_{i}")
            selected_indices = [tt.index(item) for item in selected_col2]

            if selected_col2:
                for idx, item in enumerate(selected_col2):
                    # Get the next attribute item in the list
                    next_item = tt[selected_indices[0] + 1] if selected_indices[0] + 1 < len(tt) else None
                    excluded_phrase, text_between, next_first_word = process_text(item, next_item, i, text)
                    if excluded_phrase:
                        st.write(f"**Excluded Words:** {excluded_phrase}")
                        st.write(f"**Text Between Excluded Words and Next First Word:** {text_between}")
                        st.write(f"**First Word of Next Item:** {next_first_word}")

    # Button to add a new row
    if st.button("Add Row"):
        st.session_state.num_rows += 1
        st.rerun()  # Refresh the app to show the new row

    csv_file = "saved_data.csv"
    fieldnames = ["Excluded Words", "Next Word"]

    if st.button(f"Save Row {i+1} to CSV"):
                            with open(csv_file, mode="a", newline="") as f:
                                writer = csv.DictWriter(f, fieldnames=fieldnames)
                                writer.writerow({"Excluded Words": excluded_phrase, "Next Word": next_first_word})
                                st.success(f"Row {i+1} saved to CSV.")







    # Initialize session state for number of rows
    # import streamlit as st
    # import re

    # # Initialize session state for number of rows
    # if "num_rows" not in st.session_state:
    #     st.session_state.num_rows = 1  # Start with 1 row

    # # Define the list of attributes for Column 1
    # tttt = ["A", "B", "C", "D"]

    # # Define the list of attribute items for Column 2 (Example Data)
    # # tt = ["Alpha Beta Gamma", "Red Blue Green", "Hello World Streamlit", "Python Java C++"]

    # st.write("### Dynamic Multi-Select Table")

    # # Function to exclude words and find the next word after exclusion
    # def process_text(selected_text, row_index, tt):
    #     words = selected_text.split(" ")  # Split text into words
    #     words2 = " ".join(tt)
    #     excluded_words = st.multiselect(f"Select words to exclude (Row {row_index+1}):", words, key=f"exclude_{row_index}_{selected_text}")

    #     if excluded_words:
    #         # Join the excluded words into a phrase
    #         excluded_phrase = " ".join(excluded_words)

    #         # Create regex pattern to find the word after the excluded words
    #         pattern = rf"{re.escape(excluded_phrase)}\s+(\w+)"  # Looks for a word right after the excluded phrase
    #         match = re.search(pattern, words2)

    #         if match:
    #             next_word = match.group(1)  # Get the word after the excluded phrase
    #         else:
    #             next_word = "No word found after exclusion"

    #         return excluded_phrase, next_word
    #     return None, None

    # # Display existing rows
    # for i in range(st.session_state.num_rows):
    #     col1, col2 = st.columns(2)

    #     with col1:
    #         st.multiselect(f"Attribute (Row {i+1}):", tttt, key=f"col1_{i}")

    #     with col2:
    #         selected_col2 = st.multiselect(f"Select Attribute Item (Row {i+1}):", tt, key=f"col2_{i}")

    #         if selected_col2:
    #             for item in selected_col2:
    #                 excluded_phrase, next_word = process_text(item, i,tt)
    #                 if excluded_phrase:
    #                     st.write(f"**Excluded Words:** {excluded_phrase}")
    #                     st.write(f"**Word after Excluded Words:** {next_word}")

    # # Button to add a new row
    # if st.button("Add Row"):
    #     st.session_state.num_rows += 1
    #     st.rerun()  # Refresh the app to show the new row








    # if "num_rows" not in st.session_state:
    #     st.session_state.num_rows = 1  # Start with 1 row

    # # Define the list of items to select from in column 1
    # tttt = ["A", "B", "C", "D"]

    # st.write("### Dynamic Multi-Select Table")

    # # Function to handle word exclusion logic
    # def exclude_words(selected_item):
    #     # Split the selected item by spaces (or other delimiters if needed)
    #     words = selected_item.split(" ")
    #     # Generate a multi-select box with the words for exclusion
    #     excluded_words = st.multiselect("Select words to exclude:", words)
    #     remaining_words = [word for word in words if word not in excluded_words]
    #     return remaining_words

    # # Display existing rows
    # for i in range(st.session_state.num_rows):
    #     col1, col2 = st.columns(2)
        
    #     with col1:
    #         st.multiselect(f"Attribute (Row {i+1}):", tttt, key=f"col1_{i}")
        
    #     with col2:
    #         selected_col2 = st.multiselect(f"Select Attribute Item (Row {i+1}):", tt, key=f"col2_{i}")
    #         if selected_col2:
    #             # For each selection in col2, split and allow word exclusion
    #             for item in selected_col2:
    #                 remaining_words = exclude_words(item)
    #                 if remaining_words:
    #                     st.write(f"Remaining words for {item}: {', '.join(remaining_words)}")
    #                 else:
    #                     st.write(f"All words in {item} were excluded.")

    # # Button to add a new row
    # if st.button("Add Row"):
    #     st.session_state.num_rows += 1
    #     st.rerun()  # Refresh the app to show the new row



    if match:
        extracted_text = match.group(1).strip().replace(",", "")
        # print(match)

        item_pattern = re.compile(r'(\d+)\s+([A-Za-z0-9\s\-]+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)', re.IGNORECASE)
        data = []
        

        for line in extracted_text.split("\n"):
           
            match = item_pattern.match(line)

            if match:
                # print(match.groups())
                a, b, c, d, e, f, g = match.groups()

                invoice_number = re.search(r'Invoice No[:\s]*(\S+)', text)
                doc_date = re.search(r'Document Date[:\s]*([A-Za-z0-9\s\-]+)\s', text)
                acc_num = re.search(r'Account No[:\s]*([A-Za-z0-9\s\-]+)\s', text)

                grade_match = re.search(r'MBIC[:\s]*(\S+)', text)
                silo_match = re.search(r'(\S+)\s+Siloco', text)
                
                invoice_number = invoice_number.group(1) if invoice_number else None
                acc_num = acc_num.group(1) if acc_num else None
                doc_date = doc_date.group(1) if doc_date else None
                grade = grade_match.group(1) if grade_match else None
                silo = silo_match.group(1) if silo_match else None
                crop = b.split(" ")[-1]
                commodity = " ".join(b.split(" ")[:2])

                data.append([b, c, d, e, f, g, grade, silo, crop, commodity, invoice_number, doc_date, acc_num])

        return pd.DataFrame(data, columns=["Description", "Quantity", "Unit Price", "Total (Excl.)", "VAT", "Total (Incl.)", "Grade", "Cost Type", "Crop", "Commodity", "invnum","doc_date", "acc_num"])

    return pd.DataFrame()

# Function to extract structured data for BKB format
def extract_bkb_data(text, start, end):
    import re, csv
    pattern = re.compile(rf'{re.escape(start)}\s*\n(.*?)\n\s*{re.escape(end)}', re.DOTALL | re.IGNORECASE)
    match = pattern.search(text)
    print(text)



    tt = text.split("\n")

    # Initialize session state for number of rows
    if "num_rows" not in st.session_state:
        st.session_state.num_rows = 1  # Start with 1 row

    # Define the list of attributes for Column 1
    tttt = ["A", "B", "C", "D"]

    # Define the list of attribute items for Column 2 (Example Data)

    st.write("### Dynamic Multi-Select Table")

    # Function to exclude words, find the next first word and extract text between exclusions
    def process_text(selected_text, next_text, row_index, text):
        words = selected_text.split(" ")  # Split text into words
        excluded_words = st.multiselect(f"Select words to exclude (Row {row_index+1}):", words, key=f"exclude_{row_index}_{selected_text}")

        if excluded_words:
            # Join the excluded words into a phrase
            excluded_phrase = " ".join(excluded_words)

            # Find the first word of the next attribute item
            next_first_word = next_text.split(" ")[0] if next_text else None

            # Regex to find everything between excluded phrase and next first word
            if next_first_word:
                pattern = rf"{re.escape(excluded_phrase)}\s+(.*?)\s+{re.escape(next_first_word)}"
                match = re.search(pattern, text)
                if match:
                    text_between = match.group(1)  # Extract text between the exclusions and the next word
                else:
                    text_between = "No text found between exclusions and next first word"
            else:
                text_between = "Next attribute not available"

            return excluded_phrase, text_between, next_first_word
        return None, None, None
    

    # Display existing rows
    for i in range(st.session_state.num_rows):
        col1, col2 = st.columns(2)

        with col1:
            attribute = st.multiselect(f"Attribute (Row {i+1}):", tttt, key=f"col1_{i}")

        with col2:
            selected_col2 = st.multiselect(f"Select Attribute Item (Row {i+1}):", tt, key=f"col2_{i}")

            ff = []
            selected_colw = ff.append(selected_col2[1])
            selected_indices = [tt.index(item) for item in selected_colw]

            if selected_indices:
                for idx, item in enumerate(selected_col2):
                    # Get the next attribute item in the list
                    next_item = tt[selected_indices[0] + 1] if selected_indices[0] + 1 < len(tt) else None
                    excluded_phrase, text_between, next_first_word = process_text(item, next_item, i, text)
                    if excluded_phrase:
                        st.write(f"**Excluded Words:** {excluded_phrase}")
                        st.write(f"**Text Between Excluded Words and Next First Word:** {text_between}")
                        st.write(f"**First Word of Next Item:** {next_first_word}")

    # Button to add a new row
    if st.button("Add Row"):
        st.session_state.num_rows += 1
        st.rerun()  # Refresh the app to show the new row

    csv_file = "saved_data.csv"
    fieldnames = ["Excluded Words", "Next Word"]

    if st.button(f"Save Row {i+1} to CSV"):
                            with open(csv_file, mode="a", newline="") as f:
                                writer = csv.DictWriter(f, fieldnames=fieldnames)
                                writer.writerow({"Excluded Words": excluded_phrase, "Next Word": next_first_word})
                                st.success(f"Row {i+1} saved to CSV.")



    if match:
        extracted_text = match.group(1).strip()
        item_pattern = re.compile(r'([A-Za-z0-9\s]+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)', re.IGNORECASE)
        data = []

        for line in extracted_text.split("\n"):
            match = item_pattern.match(line)
            if match:
                a, b, c, d = match.groups()
                data.append([None, a, None, None, None, None, b, c, d])
            else:
                charge_match = re.match(r'(\S+)\s+(.+?)\s+(\d+\.\d+)\s+(\S+)\s+(\d+\.\d+)\s+(\d+\.\d+)', line)
                if charge_match:
                    scode, description, num1, num2, num3, dsds = charge_match.groups()
                    branch = re.search(r'Branch\s+(\S+)', text)
                    silo = branch.group(1) if branch else None
                    silo2 = branch
                    lld = description.split(" ")
                    data.append([scode, description, lld[0], lld[2], num1, num3, dsds, None, None, silo2 if num3 else None])
                # else:
                #     data.append([None, line, None, None, None, None])

        return pd.DataFrame(data, columns=["Stock Code", "Description", "Crop", "Grade", "Quantity", "Rate", "Sub-Total", "VAT", "Total", "Cost Type"])

    return pd.DataFrame()

def extract_overberg_data(text, start, end):
    pattern = re.compile(rf'{re.escape(start)}\s*\n(.*?)\n\s*{re.escape(end)}', re.DOTALL | re.IGNORECASE)
    match = pattern.search(text)

    if match:
        extracted_text = match.group(1).strip()
        print(extracted_text)
        item_pattern = re.compile(r'([A-Za-z0-9\s]+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)',re.DOTALL | re.IGNORECASE)
        data = []

        for line in extracted_text.split("\n"):
            match = item_pattern.match(line)
            if match:
                print(match.group(0))
                print(match.group(1))
                print(match.group(2))
                print(match.group(3))
        
                # print(match.groups())
                a, b, c, d,t,y = match.groups()
                data.append([None, a, None, None, None, None, b, c, d])
            else:
                charge_match = re.match(r'(\d{1,3}(?:[ ,]?\d{3})*(?:\.\d+)?)\s+(\d+)\s+([A-Za-z0-9\s\-]+)\s+([\d,.]+)\s+(\d{1,3}(?:[ ,]?\d{3})*(?:\.\d+)?)\s+(\d{1,3}(?:[ ,]?\d{3})*(?:\.\d+)?)', line)
                if charge_match:
                    print(charge_match.groups())
                    scode, num1, description, num2, num3, dsds = charge_match.groups()
                    lld = description.split(" ")
                    silo = lld[-1]
                    data.append([scode, description, lld[0], silo, num1, num3, dsds, None, None, silo if num3 else None])
                # else:
                #     data.append([None, line, None, None, None, None])

        return pd.DataFrame(data, columns=["Stock Code", "Description", "Crop", "Grade", "Quantity", "Rate", "Sub-Total", "VAT", "Total", "Cost Type"])

    return pd.DataFrame()

# Streamlit UI
st.title("Extract Structured Data from PDFs")

# Upload multiple PDFs
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

# Choose processing type
data_type = st.radio("Select the data type to extract:", ["AFGRI", "BKB", "OVERBERG"])

if uploaded_files:
    start = st.text_input("Enter start pattern for extraction")
    end = st.text_input("Enter end pattern for extraction")

    if start and end:
        all_dfs = []

        for pdf_file in uploaded_files:
            text = extract_text_from_pdf(pdf_file)

            if data_type == "AFGRI":
                df = extract_afgri_data(text, start, end)
            elif data_type == "OVERBERG":
                df = extract_overberg_data(text, start, end)
            else:
                df = extract_bkb_data(text, start, end)

            all_dfs.append(df)

        if all_dfs:
            final_df = pd.concat(all_dfs, ignore_index=True)
            st.write(final_df)

            # Download as CSV
            csv = final_df.to_csv(index=False).encode("utf-8")
            st.download_button(label="Download CSV", data=csv, file_name="extracted_data.csv", mime="text/csv")
