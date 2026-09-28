from app.graph.state import GraphState


def main():
    state: GraphState = {
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
    print("LANGGRAPH STATE TEST")
    print("=" * 70)
    print()

    print("Initial state:")
    for key, value in state.items():
        print(f"{key}: {value}")

    print()

    # Simulate what the rewrite node will eventually do.
    state["search_query"] = (
        "TCP slow start congestion window growth"
    )
    state["rewrite_count"] += 1

    print("After simulated rewrite:")
    print(f"question:     {state['question']}")
    print(f"search_query: {state['search_query']}")
    print(f"rewrite_count: {state['rewrite_count']}")

    print()

    # The original question must never change.
    assert state["question"] == (
        "How does TCP slow start work?"
    )

    assert state["search_query"] == (
        "TCP slow start congestion window growth"
    )

    assert state["rewrite_count"] == 1

    print("Original question preserved: PASS")
    print("Search query updated: PASS")
    print("Rewrite count updated: PASS")
    print()
    print("All graph state tests passed.")


if __name__ == "__main__":
    main()