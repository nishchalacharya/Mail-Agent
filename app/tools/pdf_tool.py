# app/tools/pdf_tool.py

from PyPDF2 import PdfReader


def parse_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.strip() or "No text found in PDF"
