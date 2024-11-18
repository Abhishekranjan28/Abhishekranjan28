import streamlit as st
import os
import tempfile
import fitz  # PyMuPDF for PDF text extraction
from docx import Document  # Library to handle .docx files
import pandas as pd

# CSV file path for data storage
CSV_FILE_PATH = "extracted_data.csv"

# Function to initialize the CSV file if it doesn't exist
def initialize_csv_file():
    if not os.path.exists(CSV_FILE_PATH):
        # Create an empty DataFrame and save it as a CSV file
        df = pd.DataFrame(columns=["Company Name", "Product Brand", "Product Description", "Production Location",
                                   "Geographical Area", "Production Volume", "Annual Revenue", "Extracted Text"])
        df.to_csv(CSV_FILE_PATH, index=False)

# Function to append data to the CSV file
def append_to_csv(data):
    # Load existing data
    df = pd.read_csv(CSV_FILE_PATH)
    
    # Append the new row
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    
    # Save back to CSV
    df.to_csv(CSV_FILE_PATH, index=False)

# Initialize the CSV file if it doesn't exist
initialize_csv_file()

st.markdown(
    """
    <h1 style='font-size:24px; color:black;'>Data Extractor and CSV Saver</h1>
    """,
    unsafe_allow_html=True
)

# File uploader
uploaded_files = st.file_uploader(
    "Upload files (PDF, text, or Word documents):",
    type=["pdf", "txt", "docx"],
    accept_multiple_files=True,
)

extracted_text = ""
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        try:
            if file_extension == "pdf":
                with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf_file:
                    for page_num in range(pdf_file.page_count):
                        page = pdf_file[page_num]
                        extracted_text += page.get_text("text") + "\n"
            elif file_extension == "txt":
                extracted_text += uploaded_file.read().decode("utf-8") + "\n"
            elif file_extension == "docx":
                doc = Document(uploaded_file)
                for para in doc.paragraphs:
                    extracted_text += para.text + "\n"
        except Exception as e:
            st.error(f"Error processing file '{uploaded_file.name}': {str(e)}")

# Input fields
col1, col2 = st.columns(2)
with col1:
    company_name = st.text_input("Enter the name of the company:")
    product_brand = st.text_input("Enter the product brand:")
    product_description = st.text_input("Enter the product description:")
with col2:
    production_location = st.text_input("Enter the production location:")
    geographical_area = st.text_input("Enter the geographical market:")
    production_volume = st.text_input("Enter the production volume:")
    annual_revenue = st.text_input("Enter the annual revenue:")

if st.button("Save Data to CSV"):
    if not company_name or not product_brand or not product_description or not production_location or not geographical_area or not production_volume or not annual_revenue:
        st.warning("Please fill out all required fields.")
    else:
        data = {
            "Company Name": company_name,
            "Product Brand": product_brand,
            "Product Description": product_description,
            "Production Location": production_location,
            "Geographical Area": geographical_area,
            "Production Volume": production_volume,
            "Annual Revenue": annual_revenue,
            "Extracted Text": extracted_text
        }
        append_to_csv(data)
        st.success("Data saved successfully to CSV file.")

        # Provide a download button for the CSV file
        with open(CSV_FILE_PATH, "rb") as csv_file:
            st.download_button(
                "Download CSV File",
                csv_file,
                file_name="extracted_data.csv",
                mime="text/csv"
            )
