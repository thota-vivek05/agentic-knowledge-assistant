from collections import Counter

from app.ingestion.processor import process_documents


folder_path = "data/raw"

pages = process_documents(folder_path)

print("\n" + "=" * 80)
print("INGESTION SUMMARY")
print("=" * 80)

print(f"Total pages processed: {len(pages)}")

sources = Counter(
    page["metadata"]["source"]
    for page in pages
)

print("\nPages by source:")

for source, count in sources.items():
    print(f"  {source}: {count} page(s)")

print("\nExtraction methods:")

methods = Counter(
    page["metadata"]["extraction_method"]
    for page in pages
)

for method, count in methods.items():
    print(f"  {method}: {count}")