from app.graph.workflow import build_retry_graph
from app.rag.prompt import NOT_FOUND_MESSAGE


def main():
    print("=" * 70)
    print("FALLBACK INTEGRATION TEST")
    print("=" * 70)
    print()

    question = "What is TCP CUBIC?"

    initial_state = {
        "question": question,
        "search_query": question,
        "documents": [],
        "relevant_documents": [],
        "sufficient": False,
        "grade_reason": "",
        "rewrite_count": 0,
        "answer": "",
        "answered": False,
    }

    print(f"Question: {question}")
    print()
    print("Running corrective RAG graph...")
    print()

    graph = build_retry_graph()

    result = graph.invoke(initial_state)

    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"Original question:")
    print(f"  {result['question']}")

    print()
    print(f"Final search query:")
    print(f"  {result['search_query']}")

    print()
    print(f"Rewrite count:")
    print(f"  {result['rewrite_count']}")

    print()
    print(f"Sufficient:")
    print(f"  {result['sufficient']}")

    print()
    print(f"Answered:")
    print(f"  {result['answered']}")

    print()
    print("Answer:")
    print(result["answer"])

    print()

    assert result["question"] == question
    assert result["sufficient"] is False
    assert result["answered"] is False
    assert result["answer"] == NOT_FOUND_MESSAGE
    assert result["rewrite_count"] <= 2

    print("Original question preserved: PASS")
    print("Evidence remained insufficient: PASS")
    print("Answered flag is False: PASS")
    print("Exact fallback message returned: PASS")
    print("Rewrite limit respected: PASS")

    print()
    print("Fallback integration test passed.")


if __name__ == "__main__":
    main()