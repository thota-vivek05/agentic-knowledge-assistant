from app.graph.workflow import build_retry_graph


def main():
    print("=" * 70)
    print("RETRY GRAPH TEST")
    print("=" * 70)
    print()

    graph = build_retry_graph()

    initial_state = {
        "question": "How does TCP work when congestion happens?",
        "search_query": "How does TCP work when congestion happens?",
        "documents": [],
        "relevant_documents": [],
        "sufficient": False,
        "grade_reason": "",
        "rewrite_count": 0,
        "answer": "",
        "answered": False,
    }

    print("Running graph...")
    print()

    result = graph.invoke(initial_state)

    print("=" * 70)
    print("GRAPH RESULTS")
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
    print(f"Grade reason:")
    print(f"  {result['grade_reason']}")

    print()

    assert result["question"] == initial_state["question"]
    assert result["rewrite_count"] <= 2

    print("Original question preserved: PASS")
    print("Rewrite limit respected: PASS")

    if result["sufficient"]:
        print("Graph ended through successful retrieval: PASS")
    else:
        print("Graph ended without sufficient evidence: PASS")

    print()
    print("Retry graph test passed.")


if __name__ == "__main__":
    main()