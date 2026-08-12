# Responsible for:

# JPG / PNG
#     ↓
# OCR
#     ↓
# text

from pathlib import Path

import pytesseract
from PIL import Image


def extract_text_from_image(file_path: str) -> dict:
    """
    Extract text from an image using Tesseract OCR.
    """

    image = Image.open(file_path)

    text = pytesseract.image_to_string(image).strip()

    return {
        "text": text,
        "metadata": {
            "source": Path(file_path).name,
            "page": 1,
            "type": "image",
            "extraction_method": "tesseract",
        },
    }