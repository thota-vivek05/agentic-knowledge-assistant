from app.graph.nodes import generate_node
from app.rag.chain import retrieve_documents


def main():
    print("=" * 70)
    print("GENERATE NODE TEST")
    print("=" * 70)
    print()

    question = "How does TCP slow start work?"

    documents = retrieve_documents(
        question,
        k=3,
    )

    state = {
        "question": question,
        "search_query": question,
        "documents": documents,
        "relevant_documents": documents,
        "sufficient": True,
        "grade_reason": "Evidence is sufficient.",
        "rewrite_count": 0,
        "answer": "",
        "answered": False,
    }

    print(f"Retrieved documents: {len(documents)}")
    print()
    print("Running generate node...")

    result = generate_node(state)

    print()
    print("=" * 70)
    print("RESULT")
    print("=" * 70)

    print("Answer:")
    print(result["answer"])

    print()
    print(f"Answered: {result['answered']}")

    assert isinstance(result["answer"], str)
    assert result["answer"].strip()
    assert result["answered"] is True

    print()
    print("Answer generated: PASS")
    print("Answered flag is True: PASS")
    print()
    print("Generate node test passed.")


if __name__ == "__main__":
    main()