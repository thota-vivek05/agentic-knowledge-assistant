from app.ingestion.processor import process_document
from app.chunking.splitter import chunk_pages
from app.vector_store.chroma import (
    create_vectorstore,
    add_chunks,
)


PDF_PATH = "data/raw/congestion_control.pdf"


print("=" * 80)
print("CHROMADB REAL CHUNK TEST")
print("=" * 80)


# ------------------------------------------------------------------
# 1. Ingest document
# ------------------------------------------------------------------

print("\n[1] Processing document...")

pages = process_document(PDF_PATH)

print(f"Pages extracted: {len(pages)}")


# ------------------------------------------------------------------
# 2. Create chunks
# ------------------------------------------------------------------

print("\n[2] Creating chunks...")

chunks = chunk_pages(pages)

print(f"Chunks created: {len(chunks)}")


# ------------------------------------------------------------------
# 3. Index all chunks from the document.
# ------------------------------------------------------------------

chunks_to_index = chunks

print(f"Chunks to index: {len(chunks_to_index)}")


# ------------------------------------------------------------------
# 4. Create ChromaDB
# ------------------------------------------------------------------

print("\n[3] Creating ChromaDB...")

vectorstore = create_vectorstore()


# ------------------------------------------------------------------
# 5. Add chunks
# ------------------------------------------------------------------

print("\n[4] Adding chunks to ChromaDB...")

document_ids = add_chunks(
    vectorstore,
    chunks_to_index,
)

print("Chunks indexed successfully.")

collection_data = vectorstore.get()

print(f"\nDocuments currently in ChromaDB: {len(collection_data['ids'])}")

print("\nGenerated IDs:")

for document_id in document_ids:
    print(document_id)


# ------------------------------------------------------------------
# 6. Similarity search
# ------------------------------------------------------------------

query = "How does TCP slow start work?"

print("\n[5] Performing similarity search...")
print(f"Query: {query}")

results = vectorstore.similarity_search(
    query,
    k=3,
)


# ------------------------------------------------------------------
# 7. Display results
# ------------------------------------------------------------------

print("\nRetrieved results:")

for i, result in enumerate(results, start=1):

    print("\n" + "-" * 80)

    print(f"Result {i}")

    print("\nContent:")
    print(result.page_content[:500])

    print("\nMetadata:")
    print(result.metadata)