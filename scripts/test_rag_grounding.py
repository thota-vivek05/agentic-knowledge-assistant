from app.rag.chain import answer_question
from app.rag.prompt import NOT_FOUND_MESSAGE


TEST_CASES = [
    {
        "question": "How does TCP slow start work?",
        "should_answer": True,
    },
    {
        "question": "What is the capital of France?",
        "should_answer": False,
    },
    {
        "question": "How does TCP CUBIC work?",
        "should_answer": False,
    },
    {
        "question": "What is TCP BBR?",
        "should_answer": False,
    },
]


def main():

    passed = 0

    print("=" * 70)
    print("RAG GROUNDING EVALUATION")
    print("=" * 70)
    print()

    for index, test_case in enumerate(
        TEST_CASES,
        start=1,
    ):

        question = test_case["question"]
        should_answer = test_case["should_answer"]

        result = answer_question(
            question,
            k=3,
        )

        answered = result["answered"]

        passed_test = (
            answered == should_answer
        )

        if passed_test:
            passed += 1

        status = (
            "PASS"
            if passed_test
            else "FAIL"
        )

        print(
            f"{index}. {status} - {question}"
        )

        print(
            f"   Expected answer: "
            f"{should_answer}"
        )

        print(
            f"   Actual answer:   "
            f"{answered}"
        )

        print(
            f"   Response: "
            f"{result['answer']}"
        )

        if result["documents"]:

            print("   Sources:")

            for document in result["documents"]:

                metadata = document.metadata

                print(
                    f"      - "
                    f"{metadata.get('source', 'Unknown source')} "
                    f"(chunk "
                    f"{metadata.get('chunk_index', 'unknown')})"
                )

        else:

            print("   Sources: none")

        print()

    total = len(TEST_CASES)

    print("=" * 70)
    print("GROUNDING RESULTS")
    print("=" * 70)

    print(
        f"Passed: {passed}/{total}"
    )

    print(
        f"Accuracy: "
        f"{passed / total * 100:.2f}%"
    )

    if passed == total:
        print("All grounding tests passed.")
    else:
        print("Some grounding tests failed.")

    print()

    print(
        "Expected refusal message:"
    )
    print(
        NOT_FOUND_MESSAGE
    )


if __name__ == "__main__":
    main()