# Responsible for:
# Typed PDF → text
# Scanned PDF → images → OCR

from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from pypdf import PdfReader


MIN_TEXT_LENGTH = 100


def ocr_pdf_page(file_path: str, page_number: int) -> str:
    """
    Convert one PDF page to an image and extract text using Tesseract OCR.
    """

    images = convert_from_path(
        file_path,
        dpi=200,
        first_page=page_number,
        last_page=page_number,
    )

    if not images:
        return ""

    return pytesseract.image_to_string(images[0])


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extract text from a PDF.

    Uses pypdf for pages containing sufficient text.
    Falls back to Tesseract OCR for pages where the native
    PDF text is insufficient and the page contains images.
    """

    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        # First attempt: native PDF text extraction
        text = page.extract_text() or ""
        text = text.strip()

        # Keep the original pypdf result for our decision.
        native_text_length = len(text)

        # Check whether the PDF page contains images.
        has_images = len(page.images) > 0

        # Default extraction method
        extraction_method = "pypdf"

        # Use OCR only when:
        # 1. Native text is insufficient
        # 2. The page contains an image
        if native_text_length < MIN_TEXT_LENGTH and has_images:

            print(
                f"Page {page_number}: insufficient native text "
                f"({native_text_length} characters) and contains images. "
                f"Using OCR..."
            )

            text = ocr_pdf_page(
                file_path,
                page_number,
            ).strip()

            extraction_method = "tesseract"

        pages.append(
            {
                "text": text,
                "metadata": {
                    "source": Path(file_path).name,
                    "page": page_number,
                    "type": "pdf",
                    "extraction_method": extraction_method,
                },
            }
        )

    return pages


"""we are returning in json format because the page information is critical for our eventual citations."""