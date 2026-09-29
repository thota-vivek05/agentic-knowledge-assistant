from app.graph.edges import MAX_REWRITES, route_after_grade


def main():
    print("=" * 70)
    print("RETRY LIMIT TEST")
    print("=" * 70)
    print()

    rewrite_count = 0
    retrieval_count = 0
    rewrite_count_observed = 0

    while True:
        # Simulate a retrieval attempt.
        retrieval_count += 1

        print(
            f"Retrieval attempt: {retrieval_count}"
        )

        # Simulate a grader that ALWAYS says
        # the retrieved evidence is insufficient.
        sufficient = False

        state = {
            "question": "Test question",
            "search_query": "Test search query",
            "documents": [],
            "relevant_documents": [],
            "sufficient": sufficient,
            "grade_reason": "Fake grader: insufficient evidence.",
            "rewrite_count": rewrite_count,
            "answer": "",
            "answered": False,
        }

        route = route_after_grade(state)

        print(
            f"Route: {route}"
        )

        if route == "fallback":
            print()
            print("Fallback reached.")
            break

        assert route == "rewrite"

        rewrite_count += 1
        rewrite_count_observed += 1

        print(
            f"Rewrite performed: {rewrite_count}"
        )
        print()

    print("=" * 70)
    print("RETRY LIMIT RESULTS")
    print("=" * 70)

    print(
        f"Expected maximum retrieval attempts: "
        f"{MAX_REWRITES + 1}"
    )

    print(
        f"Actual retrieval attempts: "
        f"{retrieval_count}"
    )

    print(
        f"Expected rewrites: "
        f"{MAX_REWRITES}"
    )

    print(
        f"Actual rewrites: "
        f"{rewrite_count_observed}"
    )

    assert retrieval_count == MAX_REWRITES + 1
    assert rewrite_count_observed == MAX_REWRITES

    print()
    print("Retrieval attempt limit: PASS")
    print("Rewrite limit: PASS")
    print("Fallback reached: PASS")
    print()
    print("Retry limit test passed.")


if __name__ == "__main__":
    main()