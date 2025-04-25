#!/usr/bin/env python3
import openai

import fitz  # PyMuPDF for PDF processing
import ollama
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_path):
    """Extract text from a given PDF file."""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def process_text_with_phi3(text):
    """Use Ollama with Phi-3 to process extracted text."""
    response = ollama.chat(model="phi3", messages=[{"role": "user", "content": text}])
    return response["message"]["content"]

def ocr_pdf(pdf_path):
    """Perform OCR using Tesseract."""
    doc = fitz.open(pdf_path)
    extracted_text = ""
    
    for page_num in range(len(doc)):
        pix = doc[page_num].get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        extracted_text += pytesseract.image_to_string(img) + "\n"
    
    return extracted_text

def main(pdf_path):
    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text.strip():  # If no text, perform OCR
        extracted_text = ocr_pdf(pdf_path)
    print("Extracted Text:",extracted_text)
    print("------------------------------------   ----------------------------------------------------------------------------------------------------------------------------")
    summary = process_text_with_phi3( "Provide a summary of the following text:"+"\n"+extracted_text)
    key_details = process_text_with_phi3( "Provide a list of key details of the text"+"\n"+extracted_text)
    answer = process_text_with_phi3("If there are any questions , provide answers for the following text "+"\n"+extracted_text)
    
    print("Summary:\n", summary)
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("\nKey Details:\n", key_details)
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("\nQ&A:\n",answer)

if __name__ == "__main__":
    test_pdf = "Pdf/HLGUA2TVCFAMJQDFC5IC43JBVUOFXDWB.pdf"  
    main(test_pdf)