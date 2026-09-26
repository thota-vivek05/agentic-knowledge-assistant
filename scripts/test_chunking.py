from app.chunking.splitter import chunk_pages
from app.ingestion.processor import process_document


file_path = "data/raw/Operating System!.pdf"


# Phase 1: extract pages
pages = process_document(file_path)

# Phase 2: create chunks
chunks = chunk_pages(pages)


print("=" * 80)
print("CHUNKING SUMMARY")
print("=" * 80)

print(f"Pages: {len(pages)}")
print(f"Chunks: {len(chunks)}")


if not chunks:
    print("\nNo chunks were created.")
    raise SystemExit


# Chunk statistics
lengths = [len(chunk["text"]) for chunk in chunks]

print("\nChunk statistics:")
print(f"Minimum characters: {min(lengths)}")
print(f"Maximum characters: {max(lengths)}")
print(f"Average characters: {sum(lengths) / len(lengths):.2f}")


# Display first 5 chunks
print("\nFirst 5 chunks:\n")

for chunk in chunks[:5]:

    print("=" * 80)

    metadata = chunk["metadata"]

    print(
        f"Source: {metadata['source']} | "
        f"Pages: {metadata['start_page']}-"
        f"{metadata['end_page']} | "
        f"Chunk: {metadata['chunk_index']}"
    )

    print(f"Characters: {len(chunk['text'])}")

    print("-" * 80)

    print(chunk["text"])