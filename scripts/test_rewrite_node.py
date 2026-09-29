from app.graph.rewrite import rewrite_query


def main():
    print("=" * 70)
    print("QUERY REWRITE NODE TEST")
    print("=" * 70)
    print()

    original_question = (
        "How does TCP work when congestion happens?"
    )

    original_search_query = original_question

    state = {
        "question": original_question,
        "search_query": original_search_query,
        "documents": [],
        "relevant_documents": [],
        "sufficient": False,
        "grade_reason": (
            "The retrieved documents discuss TCP generally, "
            "but they do not provide enough specific information "
            "about how TCP responds to network congestion."
        ),
        "rewrite_count": 0,
        "answer": "",
        "answered": False,
    }

    result = rewrite_query(state)

    print("Original question:")
    print(state["question"])
    print()

    print("Previous search query:")
    print(state["search_query"])
    print()

    print("Rewritten search query:")
    print(result["search_query"])
    print()

    print("Rewrite count:")
    print(result["rewrite_count"])
    print()

    assert isinstance(
        result["search_query"],
        str,
    )

    assert result["search_query"].strip()

    assert result["rewrite_count"] == 1

    # The node returns only fields it is responsible for updating.
    assert "question" not in result

    print("Search query generated: PASS")
    print("Rewrite count incremented: PASS")
    print("Original question not overwritten: PASS")
    print()
    print("Query rewrite node test passed.")


if __name__ == "__main__":
    main()