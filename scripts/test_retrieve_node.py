from app.graph.nodes import retrieve_node


def main():
    state = {
        "question": "How does TCP slow start work?",
        "search_query": "How does TCP slow start work?",
        "documents": [],
        "relevant_documents": [],
        "sufficient": False,
        "grade_reason": "",
        "rewrite_count": 0,
        "answer": "",
        "answered": False,
    }

    print("=" * 70)
    print("RETRIEVE NODE TEST")
    print("=" * 70)
    print()

    result = retrieve_node(state)

    documents = result["documents"]

    print(f"Retrieved documents: {len(documents)}")
    print()

    for index, document in enumerate(documents, start=1):
        metadata = document.metadata

        source = metadata.get("source", "Unknown")
        start_page = metadata.get("start_page", "?")
        end_page = metadata.get("end_page", "?")
        chunk_index = metadata.get("chunk_index", "?")

        print(f"{index}.")
        print(f"   Source: {source}")
        print(f"   Pages: {start_page}-{end_page}")
        print(f"   Chunk: {chunk_index}")
        print()

    assert len(documents) == 3

    for document in documents:
        assert document.page_content
        assert document.metadata.get("source")
        assert document.metadata.get("chunk_index") is not None

    print("Retrieved exactly 3 documents: PASS")
    print("Documents contain text: PASS")
    print("Documents contain metadata: PASS")
    print()
    print("Retrieve node test passed.")


if __name__ == "__main__":
    main()