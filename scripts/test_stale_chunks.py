from app.chunking.splitter import chunk_pages
from app.vector_store.chroma import create_vectorstore, add_chunks


SOURCE = "stale_test.pdf"


def create_test_chunks(count: int) -> list[dict]:
    """
    Create fake chunks for testing stale-chunk removal.
    """

    chunks = []

    for i in range(count):

        chunks.append(
            {
                "text": f"This is test chunk {i}.",
                "metadata": {
                    "source": SOURCE,
                    "start_page": i + 1,
                    "end_page": i + 1,
                    "chunk_index": i,
                    "type": "pdf",
                },
            }
        )

    return chunks


def get_source_ids(vectorstore):
    """
    Return all document IDs currently stored for SOURCE.
    """

    result = vectorstore.get(
        where={"source": SOURCE},
        include=[],
    )

    return result["ids"]


def main():

    vectorstore = create_vectorstore()

    try:

        # -----------------------------------------------------
        # Clean up anything left by a previous test run.
        # -----------------------------------------------------

        vectorstore.delete(
            where={"source": SOURCE}
        )

        print("Starting stale chunk test...")
        print()

        # -----------------------------------------------------
        # TEST 1
        # Insert 5 chunks
        # -----------------------------------------------------

        chunks_5 = create_test_chunks(5)

        ids_5 = add_chunks(
            vectorstore,
            chunks_5,
        )

        stored_ids = get_source_ids(vectorstore)

        print("After inserting 5 chunks:")
        print("Expected: 5")
        print(f"Actual:   {len(stored_ids)}")
        print()

        assert len(stored_ids) == 5

        # -----------------------------------------------------
        # TEST 2
        # Re-ingest the same 5 chunks.
        #
        # This checks idempotency.
        # -----------------------------------------------------

        add_chunks(
            vectorstore,
            chunks_5,
        )

        stored_ids = get_source_ids(vectorstore)

        print("After re-ingesting the same 5 chunks:")
        print("Expected: 5")
        print(f"Actual:   {len(stored_ids)}")
        print()

        assert len(stored_ids) == 5

        # -----------------------------------------------------
        # TEST 3
        # Shrink from 5 chunks to 3 chunks.
        #
        # chunk_3 and chunk_4 should disappear.
        # -----------------------------------------------------

        chunks_3 = create_test_chunks(3)

        ids_3 = add_chunks(
            vectorstore,
            chunks_3,
        )

        stored_ids = get_source_ids(vectorstore)

        print("After shrinking from 5 chunks to 3:")
        print("Expected: 3")
        print(f"Actual:   {len(stored_ids)}")
        print()

        assert len(stored_ids) == 3

        expected_ids = {
            f"{SOURCE}::chunk_0",
            f"{SOURCE}::chunk_1",
            f"{SOURCE}::chunk_2",
        }

        actual_ids = set(stored_ids)

        assert actual_ids == expected_ids

        print("Remaining IDs:")
        for document_id in sorted(actual_ids):
            print(f"  {document_id}")

        print()

        # -----------------------------------------------------
        # TEST 4
        # Empty input should be a no-op.
        # -----------------------------------------------------

        result = add_chunks(
            vectorstore,
            [],
        )

        stored_ids = get_source_ids(vectorstore)

        print("After add_chunks(vs, []):")
        print("Expected: 3")
        print(f"Actual:   {len(stored_ids)}")
        print()

        assert result == []
        assert len(stored_ids) == 3

        # -----------------------------------------------------
        # Final result
        # -----------------------------------------------------

        print("All stale chunk tests passed.")

    finally:

        # -----------------------------------------------------
        # ALWAYS clean up test data.
        #
        # This prevents stale_test.pdf from polluting the
        # real knowledge_base collection.
        # -----------------------------------------------------

        vectorstore.delete(
            where={"source": SOURCE}
        )

        print()
        print("Test data cleaned up.")


if __name__ == "__main__":
    main()