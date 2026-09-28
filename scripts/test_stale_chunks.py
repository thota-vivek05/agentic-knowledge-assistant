from app.vector_store.chroma import (
    create_vectorstore,
    add_chunks,
)


SOURCE = "stale_test.pdf"


def create_test_chunks(count: int) -> list[dict]:
    """Create fake chunks for testing re-indexing behavior."""

    chunks = []

    for index in range(count):

        chunks.append(
            {
                "text": (
                    f"This is test chunk {index} "
                    f"from the document."
                ),
                "metadata": {
                    "source": SOURCE,
                    "start_page": index + 1,
                    "end_page": index + 1,
                    "chunk_index": index,
                    "type": "pdf",
                },
            }
        )

    return chunks


print("=" * 80)
print("STALE CHUNK TEST")
print("=" * 80)


vectorstore = create_vectorstore()


# Remove previous test data so this test is isolated.
vectorstore.delete(
    where={"source": SOURCE}
)


print("\n[1] Indexing 5 chunks...")

chunks_v1 = create_test_chunks(5)

add_chunks(
    vectorstore,
    chunks_v1,
)

data_v1 = vectorstore.get(
    where={"source": SOURCE}
)

count_v1 = len(data_v1["ids"])

print(f"Test documents in ChromaDB: {count_v1}")


print("\n[2] Re-indexing same document with only 3 chunks...")

chunks_v2 = create_test_chunks(3)

add_chunks(
    vectorstore,
    chunks_v2,
)

data_v2 = vectorstore.get(
    where={"source": SOURCE}
)

count_v2 = len(data_v2["ids"])

print(f"Test documents in ChromaDB: {count_v2}")


print("\n[3] Checking remaining IDs...")

for document_id in sorted(data_v2["ids"]):
    print(document_id)


print("\n" + "=" * 80)
print("EXPECTED")
print("=" * 80)

print("After first indexing: 5 documents")
print("After shrinking to 3 chunks: 3 documents")


if count_v1 == 5 and count_v2 == 3:
    print("\nSTALE CHUNK TEST PASSED")
else:
    print("\nSTALE CHUNK TEST FAILED")