from app.ingestion.image_loader import extract_text_from_image


file_path = "data/raw/image.png"

result = extract_text_from_image(file_path)

print("=" * 80)
print(f"Source: {result['metadata']['source']}")
print(f"Page: {result['metadata']['page']}")
print("=" * 80)
print(result["text"])