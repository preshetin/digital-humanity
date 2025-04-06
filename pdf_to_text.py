import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

def convert_pdf_to_text(pdf_path, text_path):
  """
  Converts a PDF file to a text file, removing page numbers.

  Args:
    pdf_path (str): Path to the PDF file.
    text_path (str): Path to the output text file.
  """
  try:
    pdf_document = fitz.open(pdf_path)
    with open(text_path, "w", encoding="utf-8") as text_file:
      for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        
        # Debugging: Inspect the structure of the page content
        page_dict = page.get_text("dict")
        print(f"Page {page_num + 1} content dictionary:\n{page_dict}\n{'-'*40}")
        
        # Extract text from the "blocks" key in the dictionary
        blocks = page_dict.get("blocks", [])
        text = ""
        for block in blocks:
          if block["type"] == 0 and "lines" in block:  # Text block
            text += "\n".join(line["spans"][0]["text"] for line in block["lines"])
          elif block["type"] == 1 and "image" in block:  # Image block
            # Extract image data and perform OCR
            image_bytes = block["image"]
            image = Image.open(io.BytesIO(image_bytes))
            ocr_text = pytesseract.image_to_string(image)
            text += ocr_text

        # Debugging: Print extracted text for each page
        print(f"Page {page_num + 1} extracted text:\n{text}\n{'-'*40}")

        # Basic page number removal (customize as needed)
        lines = text.splitlines()
        filtered_lines = [line for line in lines if not (line.strip().isdigit() and len(line.strip()) <= 3)]

        text_file.write("\n".join(filtered_lines) + "\n")

    pdf_document.close()
    print(f"Successfully converted '{pdf_path}' to '{text_path}'")

  except Exception as e:
    print(f"An error occurred: {e}")

# Example usage:
pdf_file = "test-book.pdf"
text_file = "test-book.txt"
convert_pdf_to_text(pdf_file, text_file)


