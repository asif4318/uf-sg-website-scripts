import io
import os
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter


def is_text_searchable(pdf_path, output_path):
    """Checks if a PDF file is text-searchable.

    Args:
      pdf_path: The path to the PDF file.

    Returns:
      True if the PDF file is text-searchable, False otherwise.
    """
    try:
        reader = PdfReader(pdf_path)
        text = reader.pages[0].extract_text()
        print(text)
        if len(text) > 0:
            os.system(f'cp {pdf_path} {output_path}')
            print("copied")
            return True
        else:
            return False
    except:
        print("Error on " + pdf_path)
        return True  # Don't try converting


def convert_pdf_to_text_searchable(pdf_path, output_path):
    """Converts a PDF file to a text-searchable PDF file using Tesseract.

    Args:
      pdf_path: The path to the PDF file to convert.

    Returns:
      The path to the newly created text-searchable PDF file.
    """

    # Don't process pdfs that are already converted
    if os.path.isfile(output_path) == True:
        print("ALREADY CONVERTED")
        return output_path

    images = convert_from_path(pdf_path)
    pdf_pages = []
    for image in images:
        text = pytesseract.image_to_pdf_or_hocr(
            image, extension="pdf")
        pdf_pages.append(text)

    pdf_writer = PdfWriter()
    for page in pdf_pages:
        pdf = PdfReader(io.BytesIO(page))
        pdf_writer.add_page(pdf.pages[0])

    file = open(output_path, "w+b")
    pdf_writer.write(file)
    file.close()

    return output_path


def main():
    """The main function that scans a directory of PDF files and converts those that
    are not text-searchable to text-searchable PDF files using Tesseract.
    """

    input_dir = "bills"
    output_dir = "bills-converted"

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    print("Beginning loop")
    for pdf_path in os.listdir(input_dir):
        input_path = os.path.join(input_dir, pdf_path)
        output_path = os.path.join(output_dir, pdf_path)
        if not is_text_searchable(input_path, output_path):
            print("Text is not searchable")
            try:
                output_pdf_path = convert_pdf_to_text_searchable(
                    input_path, output_path)
            except:
                print("Error converting: " + input_path)
            print("Converted {} to {}.".format(input_path, output_pdf_path))


if __name__ == "__main__":
    main()
