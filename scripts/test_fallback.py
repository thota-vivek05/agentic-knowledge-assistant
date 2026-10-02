from app.graph.nodes import fallback_node
from app.rag.prompt import NOT_FOUND_MESSAGE


def main():
    print("=" * 70)
    print("FALLBACK NODE TEST")
    print("=" * 70)
    print()

    state = {
        "question": "What is TCP CUBIC?",
        "search_query": "TCP CUBIC",
        "documents": [],
        "relevant_documents": [],
        "sufficient": False,
        "grade_reason": "No relevant information found.",
        "rewrite_count": 2,
        "answer": "",
        "answered": False,
    }

    result = fallback_node(state)

    print("Fallback answer:")
    print(result["answer"])
    print()

    print("Answered:")
    print(result["answered"])
    print()

    assert result["answer"] == NOT_FOUND_MESSAGE
    assert result["answered"] is False

    print("Correct fallback message: PASS")
    print("Answered flag is False: PASS")
    print()
    print("Fallback node test passed.")


if __name__ == "__main__":
    main()