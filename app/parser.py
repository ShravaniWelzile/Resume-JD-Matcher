import pdfplumber
import re

def extract_text_from_pdf(pdf_file) ->str:
    text=" "

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text+=page_text+ "\n"

    return clean_text(text)

def clean_text(text: str)->str:
    text=re.sub(r'\s', ' ',text)
    text=re.sub(r'[^\w\s,./()-]', '', text)

    return text.strip()