from app.ingestion.pdf_loader import extract_text_from_pdf


file_path = "data/raw/DBMS!.pdf"

pages = extract_text_from_pdf(file_path)

for page in pages:
    print("=" * 80)
    print(f"Source: {page['metadata']['source']}")
    print(f"Page: {page['metadata']['page']}")
    print("=" * 80)
    print(page["text"][:1000])