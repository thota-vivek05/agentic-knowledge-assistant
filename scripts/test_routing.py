from app.graph.edges import (
    MAX_REWRITES,
    route_after_grade,
)


def make_state(
    sufficient: bool,
    rewrite_count: int,
):
    return {
        "question": "How does TCP slow start work?",
        "search_query": "How does TCP slow start work?",
        "documents": [],
        "relevant_documents": [],
        "sufficient": sufficient,
        "grade_reason": "",
        "rewrite_count": rewrite_count,
        "answer": "",
        "answered": False,
    }


def main():
    print("=" * 70)
    print("ROUTING TEST")
    print("=" * 70)
    print()

    # ---------------------------------------------------------
    # Case 1: Evidence is sufficient
    # ---------------------------------------------------------
    state = make_state(
        sufficient=True,
        rewrite_count=0,
    )

    result = route_after_grade(state)

    print("Case 1: sufficient evidence")
    print(f"Expected: generate")
    print(f"Actual:   {result}")
    assert result == "generate"
    print("PASS")
    print()

    # ---------------------------------------------------------
    # Case 2: Evidence insufficient, retries remain
    # ---------------------------------------------------------
    state = make_state(
        sufficient=False,
        rewrite_count=0,
    )

    result = route_after_grade(state)

    print("Case 2: insufficient evidence, retries available")
    print(f"Expected: rewrite")
    print(f"Actual:   {result}")
    assert result == "rewrite"
    print("PASS")
    print()

    # ---------------------------------------------------------
    # Case 3: One rewrite already happened
    # ---------------------------------------------------------
    state = make_state(
        sufficient=False,
        rewrite_count=1,
    )

    result = route_after_grade(state)

    print("Case 3: insufficient evidence, one retry remaining")
    print(f"Expected: rewrite")
    print(f"Actual:   {result}")
    assert result == "rewrite"
    print("PASS")
    print()

    # ---------------------------------------------------------
    # Case 4: Maximum rewrites reached
    # ---------------------------------------------------------
    state = make_state(
        sufficient=False,
        rewrite_count=MAX_REWRITES,
    )

    result = route_after_grade(state)

    print("Case 4: retries exhausted")
    print(f"Expected: fallback")
    print(f"Actual:   {result}")
    assert result == "fallback"
    print("PASS")
    print()

    # ---------------------------------------------------------
    # Case 5: More than maximum should still fallback
    # ---------------------------------------------------------
    state = make_state(
        sufficient=False,
        rewrite_count=MAX_REWRITES + 1,
    )

    result = route_after_grade(state)

    print("Case 5: rewrite count exceeds maximum")
    print(f"Expected: fallback")
    print(f"Actual:   {result}")
    assert result == "fallback"
    print("PASS")
    print()

    print("=" * 70)
    print("ROUTING RESULTS")
    print("=" * 70)
    print("All routing tests passed.")


if __name__ == "__main__":
    main()