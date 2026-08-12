from app.ingestion.pdf_loader import ocr_pdf_page


file_path = "data/raw/DBMS!.pdf"

text = ocr_pdf_page(file_path, page_number=1)

print("=" * 80)
print("OCR RESULT")
print("=" * 80)
print(text)