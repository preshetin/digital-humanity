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
        # print(f"Page {page_num + 1} content dictionary:\n{page_dict}\n{'-'*40}")
        
        # Extract text from the "blocks" key in the dictionary
        blocks = page_dict.get("blocks", [])
        text = ""
        for block in blocks:
          if block["type"] == 0 and "lines" in block:  # Text block
            for line in block["lines"]:
                line_text = " ".join(span["text"] for span in line["spans"])
                text += line_text + "\n"
        
        # remove extra spaces and newlines
        # text = " ".join(text.split())

        # replace double spaces with single space
        text = text.replace("  ", " ")

        # if the line has less then 8 words remove unite it with the next line
        lines = text.splitlines()
        cleaned_lines = []
        for line in lines:
            if len(line.split()) < 8 and cleaned_lines:
                cleaned_lines[-1] += " " + line.strip()
            else:
                cleaned_lines.append(line.strip())
        text = "\n".join(cleaned_lines) 
      
        

        # Debugging: Print extracted text for each page
        print(f"Page {page_num + 1} extracted text:\n{text}\n{'-'*40}")

    pdf_document.close()
    print(f"Successfully converted '{pdf_path}' to '{text_path}'")

  except Exception as e:
    print(f"An error occurred: {e}")

# Example usage:
pdf_file = "rainbow-sample.pdf"
text_file = "output-rainbow-sample.txt"
convert_pdf_to_text(pdf_file, text_file)


