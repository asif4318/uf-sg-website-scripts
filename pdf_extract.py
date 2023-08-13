import os
import pytesseract
import pdfplumber
import json
import re


def extract_bill_number(title):
    # Regular expression pattern to match the bill number format
    pattern = re.compile(r"\d\d\d\d-\d\d\d\d", re.IGNORECASE)

    match = re.search(pattern, title)
    if match:
        return "SSB " + match.group()
    else:
        return title


def extract_author_paragraphs(pdf_path):
    author_paragraphs = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[0].extract_text()
            paragraphs = text.split('\n')

            for paragraph, index in enumerate(paragraphs):
                if paragraph.lower().startswith('author'):
                    author_paragraphs.append(paragraph)
                    author_paragraphs.append(paragraphs[index+1])
    except:
        print(pdf_path)

    if len(author_paragraphs) == 0:
        res = extract_author_with_ocr(pdf_path)
        if res != "N/A":
            author_paragraphs.append(res)

    return author_paragraphs


def extract_author_with_ocr(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Convert the page to an image
            img = pdf.pages[0].to_image(resolution=300)
            img_text = pytesseract.image_to_string(
                img.original, lang='eng')  # Perform OCR
            lines = img_text.split('\n')

            for line in lines:
                if 'author' in line.lower():
                    return line.strip()
    except:
        print(pdf_path)

    return "N/A"


def extract_sponsor_paragraphs(pdf_path):
    sponsor_paragraphs = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[0].extract_text()
            paragraphs = text.split('\n')

            for paragraph in paragraphs:
                if paragraph.lower().startswith('sponsor'):
                    sponsor_paragraphs.append(paragraph)

    except:
        print(pdf_path)

    if len(sponsor_paragraphs) == 0:
        res = extract_sponsor_with_ocr(pdf_path)
        if res != "N/A":
            sponsor_paragraphs.append(res)

    return sponsor_paragraphs


def extract_sponsor_with_ocr(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Convert the page to an image
            img = pdf.pages[0].to_image(resolution=300)
            img_text = pytesseract.image_to_string(
                img.original, lang='eng')  # Perform OCR
            lines = img_text.split('\n')

            for line in lines:
                if 'sponsor' in line.lower():
                    return line.strip()
    except:
        print("ERROR: " + pdf_path)

    return "N/A"

####### Driver Code ##############


pdf_folder = 'bills-converted'

results = []

for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, filename)
        author_paragraphs = extract_author_paragraphs(pdf_path)
        sponsor_paragraphs = extract_sponsor_paragraphs(pdf_path)
        print("Extraction complete: " + filename)
        print("="*40)

        bill_info = {
            "title": filename[:-4],
            # Remove the '.pdf' extension
            "id": extract_bill_number(filename[:-4]),
            "author": "N/A" if not author_paragraphs else "".join(author_paragraphs),
            "sponsor": "N/A" if not sponsor_paragraphs else "".join(sponsor_paragraphs)
        }
        results.append(bill_info)

# Save results to a JSON file
with open('bill_results.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)

print("Results saved to bill_results.json")
