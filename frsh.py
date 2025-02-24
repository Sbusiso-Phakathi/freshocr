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
    # tt = text.split(" ")
    tt = (" ").join(text.split("\n"))
    tt = tt.split(" ")

    # Initialize session state for number of rows
    if "num_rows" not in st.session_state:
        st.session_state.num_rows = 1  # Start with 1 row

    # Define the list of attributes for Column 1
    tttt = ["A", "B", "C", "D"]
    ttx = []
    for index, i in enumerate(tt):
        ttx.append(i+str(index))
    # Define the list of attribute items for Column 2 (Example Data)

    st.write("### Dynamic Multi-Select Table")

    # Function to exclude words, find the next first word and extract text between exclusions
    def process_text(selected_text, next_text, r1,r2, text):
        tt = (" ").join(text.split("\n"))
        tt = tt.split(" ")
        selected_text = tt[r1]
        next_text = tt[r2]

        xx = tt[r1+1:r2]
        result = " ".join(xx)
        if result:
            return selected_text, result, next_text
        return None, None, None
    
    def process_text2(num, start, end, text):
        tt = (" ").join(text.split("\n"))
        tt = tt.split(" ")
        data = pd.read_csv("sasa.csv")
        
        if 1==1:
            attribute = data['Attribute'][num]

            xx = tt[start+1:end]
            result = " ".join(xx)

            return  ( attribute + ": " + result )
        return None, None, None
    
    data = pd.read_csv("sasa.csv")
    dd = data[data['Company'] == "afgri"]
    
    for ij in list(dd.index):
        start = dd['start'][ij]
        end = dd['end'][ij]
        st.write(process_text2(ij,start, end, text), key=f"hell{ij}")

    # Display existing rows
    

    for i in range(st.session_state.num_rows):
        col1, col2 = st.columns(2)

        with col1:
            attribute = st.multiselect(f"Attribute (Row {i+1}):", tttt, key=f"col1_{i}")

        with col2:
            selected_col2 = st.selectbox(f"Select Attribute Item (Row {i+1}):", ttx, key=f"col2_{i}")
            selected_indices1 = ttx.index(selected_col2)

            next_item = st.selectbox(f"Select Attribute Item ", ttx, key=f"col22_{i}")
            selected_indices2 = ttx.index(next_item)


            excluded_phrase, text_between, next_first_word = process_text(selected_col2[:-1], next_item[:-1], selected_indices1, selected_indices2, text)
            if excluded_phrase:
                        st.write(f"**Excluded Words:** {excluded_phrase}")
                        st.write(f"**Text Between Excluded Words and Next First Word:** {text_between}")
                        st.write(f"**First Word of Next Item:** {next_first_word}")

            if st.button(f"Save Row {i+1} to CSV"):
      
                df = pd.DataFrame({"Excluded Words": [excluded_phrase], "Next Word": [next_first_word], "Company": ["afgri"], "Attribute": attribute, "start": selected_indices1, "end":selected_indices2})

                # File path
                file_path = "sasa.csv"

                # Check if the CSV file already exists
                try:
                    existing_df = pd.read_csv(file_path)
                except FileNotFoundError:
                    existing_df = pd.DataFrame(columns=["Excluded Words", "Next Word", "Company"])

                # Avoid duplicates by checking if the row already exists
                if not ((existing_df["Excluded Words"] == excluded_phrase) & 
                        (existing_df["Next Word"] == next_first_word) & 
                        (existing_df["Company"] == "afgri")).any():
                    # Append the new row to the CSV without the header
                    df.to_csv(file_path, mode='a', header=False, index=True)
                else:
                    print("Duplicate row not added.")


    # Button to add a new row
    if st.button("Add Row"):
        st.session_state.num_rows += 1
        st.rerun()  # Refresh the app to show the new row



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
                for ij in range(5):
                     st.write(process_text2(ij, text), key=f"hell{ij}")

        return pd.DataFrame(data, columns=["Description", "Quantity", "Unit Price", "Total (Excl.)", "VAT", "Total (Incl.)", "Grade", "Cost Type", "Crop", "Commodity", "invnum","doc_date", "acc_num"])
        
    return pd.DataFrame()
    
# Function to extract structured data for BKB format
def extract_bkb_data(text, start, end):
    import re, csv
    pattern = re.compile(rf'{re.escape(start)}\s*\n(.*?)\n\s*{re.escape(end)}', re.DOTALL | re.IGNORECASE)
    match = pattern.search(text)
    print(text)


    tt = (" ").join(text.split("\n"))
    tt = tt.split(" ")

    # Initialize session state for number of rows
    if "num_rows" not in st.session_state:
        st.session_state.num_rows = 1  # Start with 1 row

    # Define the list of attributes for Column 1
    tttt = ["A", "B", "C", "D"]

    # Define the list of attribute items for Column 2 (Example Data)

    st.write("### Dynamic Multi-Select Table")

    # Function to exclude words, find the next first word and extract text between exclusions
    def process_text(selected_text, next_text, r1,r2, text):
        tt = (" ").join(text.split("\n"))
        tt = tt.split(" ")
        selected_text = tt[r1]
        next_text = tt[r2]

        xx = tt[r1+1:r2]
        result = " ".join(xx)
        if result:
            # Regex to find everything between excluded phrase and next first word
            if selected_text:
                pattern = rf"{re.escape(selected_text)}\s+(.*?)\s+{re.escape(next_text)}"
                match = re.search(pattern, text)
                if match:
                    text_between = match.group(1)  # Extract text between the exclusions and the next word
                else:
                    text_between = "No text found between exclusions and next first word"
            else:
                text_between = "Next attribute not available"

            return selected_text, result, next_text
        return None, None, None
    
    def process_text2(num, text):
        tt = (" ").join(text.split("\n"))
        tt = tt.split(" ")
        data = pd.read_csv("sasa.csv")
        

        if 1==1:
            excluded_phrase = data['Excluded Words'][num]
            ex = tt.index(excluded_phrase)

            next_first_word = data['Next Word'][num]
            ne = tt.index(next_first_word)

            attribute = data['Attribute'][num]

            xx = tt[ex+1:ne]
            result = " ".join(xx)

            return  ( attribute + ": " + result )
        return None, None, None
    
    data = pd.read_csv("sasa.csv")
    dd = data[data['Company'] == "bkb"]

    for ij in list(dd.index):
        st.write(process_text2(ij, text), key=f"hell{ij}")

    # Display existing rows
    for i in range(st.session_state.num_rows):
        col1, col2 = st.columns(2)

        with col1:
            attribute = st.multiselect(f"Attribute (Row {i+1}):", tttt, key=f"col1_{i}")

        with col2:
            selected_col2 = st.selectbox(f"Select Attribute Item (Row {i+1}):", tt, key=f"col2_{i}")
            selected_indices1 = tt.index(selected_col2)

            next_item = st.selectbox(f"Select Attribute Item ", tt, key=f"col22_{i}")
            selected_indices2 = tt.index(next_item)


            excluded_phrase, text_between, next_first_word = process_text(selected_col2, next_item, selected_indices1, selected_indices2, text)
            if excluded_phrase:
                        st.write(f"**Excluded Words:** {excluded_phrase}")
                        st.write(f"**Text Between Excluded Words and Next First Word:** {text_between}")
                        st.write(f"**First Word of Next Item:** {next_first_word}")

            if st.button(f"Save Row {i+1} to CSV"):
      
                df = pd.DataFrame({"Excluded Words": [excluded_phrase], "Next Word": [next_first_word], "Company": ["bkb"], "Attribute": attribute})

                # File path
                file_path = "sasa.csv"

                # Check if the CSV file already exists
                try:
                    existing_df = pd.read_csv(file_path)
                except FileNotFoundError:
                    existing_df = pd.DataFrame(columns=["Excluded Words", "Next Word", "Company"])

                # Avoid duplicates by checking if the row already exists
                if not ((existing_df["Excluded Words"] == excluded_phrase) & 
                        (existing_df["Next Word"] == next_first_word) & 
                        (existing_df["Company"] == "bkb")).any():
                    # Append the new row to the CSV without the header
                    df.to_csv(file_path, mode='a', header=False, index=True)
                else:
                    print("Duplicate row not added.")


    # Button to add a new row
    if st.button("Add Row"):
        st.session_state.num_rows += 1
        st.rerun()  # Refresh the app to show the new row



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

# Function to extract structured data for Overberg format
def extract_overberg_data(text, start, end):
    import re, csv

    pattern = re.compile(rf'{re.escape(start)}\s*\n(.*?)\n\s*{re.escape(end)}', re.DOTALL | re.IGNORECASE)
    match = pattern.search(text)

    tt = (" ").join(text.split("\n"))
    tt = tt.split(" ")

    # Initialize session state for number of rows
    if "num_rows" not in st.session_state:
        st.session_state.num_rows = 1  # Start with 1 row

    # Define the list of attributes for Column 1
    tttt = ["A", "B", "C", "D"]

    st.write("### Dynamic Multi-Select Table")

    # Function to exclude words, find the next first word and extract text between exclusions
    def process_text(selected_text, next_text, r1,r2, text):
        tt = (" ").join(text.split("\n"))
        tt = tt.split(" ")
        selected_text = tt[r1]
        next_text = tt[r2]

        xx = tt[r1+1:r2]
        result = " ".join(xx)
        if result:
            # Regex to find everything between excluded phrase and next first word
            if selected_text:
                pattern = rf"{re.escape(selected_text)}\s+(.*?)\s+{re.escape(next_text)}"
                match = re.search(pattern, text)
                if match:
                    text_between = match.group(1)  # Extract text between the exclusions and the next word
                else:
                    text_between = "No text found between exclusions and next first word"
            else:
                text_between = "Next attribute not available"

            return selected_text, result, next_text
        return None, None, None
    
    def process_text2(num, text):
        tt = (" ").join(text.split("\n"))
        tt = tt.split(" ")
        data = pd.read_csv("sasa.csv")
        dataz = []
        for kk in text.split("\n") :  
            charge_match = re.match(r'(\d{1,3}(?:[ ,]?\d{3})*(?:\.\d+)?)\s+(\d+)\s+([A-Za-z0-9\s\-]+)\s+([\d,.]+)\s+(\d{1,3}(?:[ ,]?\d{3})*(?:\.\d+)?)\s+(\d{1,3}(?:[ ,]?\d{3})*(?:\.\d+)?)', kk)
 
            if charge_match:
                print(charge_match.groups())
                scode, num1, description, num2, num3, dsds = charge_match.groups()
                lld = description.split(" ")
                silo = lld[-1]
                dataz.append([scode, description, lld[0], silo, num1, num3, dsds, None, None, silo if num3 else None])
        # return dataz
            

        if 1==1:
            excluded_phrase = data['Excluded Words'][num]
            ex = tt.index(excluded_phrase)

            next_first_word = data['Next Word'][num]
            ne = tt.index(next_first_word)

            attribute = data['Attribute'][num]

            xx = tt[ex+1:ne]
            result = " ".join(xx)

            return  ( attribute + ": " + result )
        return None, None, None
    
    data = pd.read_csv("sasa.csv")
    dd = data[data['Company'] == "overberg"]

    for ij in list(dd.index):
        st.write(process_text2(ij, text), key=f"hell{ij}")

    # Display existing rows
    for i in range(st.session_state.num_rows):
        col1, col2 = st.columns(2)

        with col1:
            attribute = st.multiselect(f"Attribute (Row {i+1}):", tttt, key=f"col1_{i}")

        with col2:
            selected_col2 = st.selectbox(f"Select Attribute Item (Row {i+1}):", tt, key=f"col2_{i}")
            selected_indices1 = tt.index(selected_col2)

            next_item = st.selectbox(f"Select Attribute Item ", tt, key=f"col22_{i}")
            selected_indices2 = tt.index(next_item)


            excluded_phrase, text_between, next_first_word = process_text(selected_col2, next_item, selected_indices1, selected_indices2, text)
            if excluded_phrase:
                        st.write(f"**Excluded Words:** {excluded_phrase}")
                        st.write(f"**Text Between Excluded Words and Next First Word:** {text_between}")
                        st.write(f"**First Word of Next Item:** {next_first_word}")

            if st.button(f"Save Row {i+1} to CSV"):
      
                df = pd.DataFrame({"Excluded Words": [excluded_phrase], "Next Word": [next_first_word], "Company": ["overberg"], "Attribute": [attribute]})

                # File path
                file_path = "sasa.csv"

                # Check if the CSV file already exists
                try:
                    existing_df = pd.read_csv(file_path)
                except FileNotFoundError:
                    existing_df = pd.DataFrame(columns=["Excluded Words", "Next Word", "Company"])

                # Avoid duplicates by checking if the row already exists
                if not ((existing_df["Excluded Words"] == excluded_phrase) & 
                        (existing_df["Next Word"] == next_first_word) & 
                        (existing_df["Company"] == "overberg")).any():
                    # Append the new row to the CSV without the header
                    df.to_csv(file_path, mode='a', header=False, index=True)
                else:
                    print("Duplicate row not added.")


    # Button to add a new row
    if st.button("Add Row"):
        st.session_state.num_rows += 1
        st.rerun()  # Refresh the app to show the new row


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
                a, b, c, d = match.groups()
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

#Letsgetgreatdevdone