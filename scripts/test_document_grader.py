from app.graph.grader import grade_documents
from app.graph.nodes import retrieve_node


TEST_CASES = [
    {
        "question": "How does TCP slow start work?",
        "expected_sufficient": True,
    },
    {
        "question": "How does TCP CUBIC work?",
        "expected_sufficient": False,
    },
]


def run_test(question: str, expected_sufficient: bool):
    state = {
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

    retrieval_result = retrieve_node(state)
    state["documents"] = retrieval_result["documents"]

    print(f"Question: {question}")
    print(
        f"Retrieved documents: "
        f"{len(state['documents'])}"
    )

    result = grade_documents(state)

    print(
        f"Sufficient: "
        f"{result['sufficient']}"
    )

    print(
        f"Relevant documents: "
        f"{len(result['relevant_documents'])}"
    )

    print(
        f"Reason: "
        f"{result['grade_reason']}"
    )

    print("Relevant chunks:")

    for document in result["relevant_documents"]:
        print(
            f"  - chunk "
            f"{document.metadata.get('chunk_index')}"
        )

    passed = (
        result["sufficient"]
        == expected_sufficient
    )

    print(
        f"Expected sufficient: "
        f"{expected_sufficient}"
    )

    print(
        f"Test: "
        f"{'PASS' if passed else 'FAIL'}"
    )

    print()

    return passed


def main():
    print("=" * 70)
    print("DOCUMENT GRADER EVALUATION")
    print("=" * 70)
    print()

    passed = 0

    for test_case in TEST_CASES:
        if run_test(
            test_case["question"],
            test_case["expected_sufficient"],
        ):
            passed += 1

    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(
        f"Passed: {passed}/{len(TEST_CASES)}"
    )

    assert passed == len(TEST_CASES)

    print()
    print("All document grader tests passed.")


if __name__ == "__main__":
    main()