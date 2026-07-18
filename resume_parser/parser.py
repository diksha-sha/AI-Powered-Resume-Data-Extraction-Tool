import pdfplumber
from docx import Document


def extract_text(file_path):
    """
    Extract text from PDF or DOCX resume.
    """

    text = ""

    # Extract text from PDF
    if file_path.lower().endswith(".pdf"):

        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")

    # Extract text from DOCX
    elif file_path.lower().endswith(".docx"):

        try:
            document = Document(file_path)

            for para in document.paragraphs:
                if para.text.strip():
                    text += para.text + "\n"

        except Exception as e:
            print(f"Error reading DOCX: {e}")

    else:
        text = "Unsupported file format."

    return text