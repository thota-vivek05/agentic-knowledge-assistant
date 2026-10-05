from app.graph.workflow import build_retry_graph


def main():
    print("=" * 70)
    print("COMPLETE CORRECTIVE RAG GRAPH TEST")
    print("=" * 70)
    print()

    question = "How does TCP slow start work?"

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
    print("Running complete corrective RAG graph...")
    print()

    graph = build_retry_graph()

    result = graph.invoke(initial_state)

    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    print("Original question:")
    print(f"  {result['question']}")

    print()
    print("Final search query:")
    print(f"  {result['search_query']}")

    print()
    print("Rewrite count:")
    print(f"  {result['rewrite_count']}")

    print()
    print("Sufficient:")
    print(f"  {result['sufficient']}")

    print()
    print("Relevant documents:")
    print(f"  {len(result['relevant_documents'])}")

    print()
    print("Answered:")
    print(f"  {result['answered']}")

    print()
    print("Answer:")
    print(result["answer"])

    print()

    assert result["question"] == question
    assert result["sufficient"] is True
    assert result["answered"] is True
    assert result["answer"].strip()
    assert len(result["relevant_documents"]) > 0
    assert result["rewrite_count"] <= 2

    print("Original question preserved: PASS")
    print("Evidence sufficient: PASS")
    print("Relevant documents selected: PASS")
    print("Answer generated: PASS")
    print("Answered flag is True: PASS")
    print("Rewrite limit respected: PASS")

    print()
    print("Complete corrective RAG graph test passed.")


if __name__ == "__main__":
    main()