# Import necessary libraries
import pytesseract
from PIL import Image
import pdfplumber
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline  # Import the transformers pipeline
import streamlit as st

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Function to extract text from an image
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [w for w in word_tokens if not w in stop_words]
    return " ".join(filtered_text)

# Initialize the transformers pipeline for text classification
classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

# Categories for classification
categories = ['Office Supplies', 'Travel', 'Software', 'Marketing']

# Function to categorize text using a pre-trained model
def categorize_text(text):
    result = classifier(text, candidate_labels=categories)
    return result['labels'][0]  # Return the most likely category

# Function to tag specific entities (e.g., dates, amounts)
def tag_entities(text):
    # Enhanced date patterns
    date_patterns = [
        r'\d{2}/\d{2}/\d{4}',  # Matches dates like 04/06/2023
        r'\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4}',  # Matches dates like 31 December 2023, 24 Apr 2024
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{1,2},\s\d{4}\b'  # Matches dates like December 31, 2023
    ]

    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text))

    # Enhanced amount patterns
    amount_patterns = [
        r'₹\s?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?',  # Matches amounts like ₹1835, ₹ 1835.00
        r'Rs\s?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?',  # Matches amounts like Rs 1500, Rs1500.00
        r'\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?'  # Matches amounts like $1835.00
    ]

    amounts = []
    for pattern in amount_patterns:
        amounts.extend(re.findall(pattern, text))

    # Ensure amounts are captured as strings with decimal points
    amounts = [amount.replace(",", "") for amount in amounts]

    # Return the first date and the last amount
    first_date = dates[0] if dates else None
    last_amount = amounts[-1] if amounts else None

    return first_date, last_amount

# Streamlit Interface
st.title("Invoice Categorization and Tagging System")

uploaded_file = st.file_uploader("Choose an image or PDF file", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_image(uploaded_file)

    preprocessed_text = preprocess_text(text)

    category = categorize_text(preprocessed_text)
    date, amount = tag_entities(text)

    st.text_area("Extracted Text", text, height=200)
    st.write(f"Categorized as: {category}")
    st.write(f"Date found: {date}")
    st.write(f"Amount found: {amount}")





