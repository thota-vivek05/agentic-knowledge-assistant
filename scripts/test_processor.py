from app.ingestion.processor import process_document


file_path = "data/raw/image.png"

pages = process_document(file_path)

print(f"Processed {len(pages)} pages\n")

for page in pages:
    print("=" * 80)
    print(f"Source: {page['metadata']['source']}")
    print(f"Page: {page['metadata']['page']}")
    print(f"Type: {page['metadata']['type']}")
    print(
        f"Extraction: "
        f"{page['metadata']['extraction_method']}"
    )
    print("=" * 80)
    print(page["text"][:500])