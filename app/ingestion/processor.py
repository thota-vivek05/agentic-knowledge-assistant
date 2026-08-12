# This will eventually be our common interface:

# Any document
#      ↓
# processor
#      ↓
# normalized documents

# So the rest of the application doesn't care whether the original input was:

# PDF
# JPG
# PNG
# scanned PDF

from pathlib import Path

from app.ingestion.image_loader import extract_text_from_image
from app.ingestion.pdf_loader import extract_text_from_pdf


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
}


def process_document(file_path: str) -> list[dict]:
    """
    Process a single supported document.

    Returns:
        List of pages containing text and metadata.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is unsupported.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Path is not a file: {file_path}"
        )

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    result = extract_text_from_image(file_path)

    return [result]


def process_documents(folder_path: str) -> list[dict]:
    """
    Process all supported documents in a folder.

    A failure in one document does not stop the remaining
    documents from being processed.

    Returns:
        List of successfully processed pages.
    """

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(
            f"Folder not found: {folder_path}"
        )

    if not folder.is_dir():
        raise ValueError(
            f"Path is not a folder: {folder_path}"
        )

    all_pages = []

    for file_path in sorted(folder.iterdir()):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            print(
                f"Skipping unsupported file: {file_path.name}"
            )
            continue

        print(
            f"\nProcessing: {file_path.name}"
        )

        try:
            pages = process_document(str(file_path))

            all_pages.extend(pages)

            print(
                f"Successfully processed "
                f"{len(pages)} page(s)"
            )

        except Exception as exc:
            print(
                f"Failed to process "
                f"{file_path.name}: {exc}"
            )

            continue

    return all_pages