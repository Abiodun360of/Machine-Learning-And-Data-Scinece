import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF resume"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_txt(txt_path):
    """Extract text from TXT resume"""
    with open(txt_path, 'r', encoding='utf-8') as f:
        return f.read()

def clean_text(text):
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep alphanumeric and basic punctuation
    text = re.sub(r'[^\w\s.,;:()\-]', '', text)
    return text.strip()