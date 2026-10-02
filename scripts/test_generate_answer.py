from app.rag.chain import (
    generate_answer,
    retrieve_documents,
)


def main():
    print("=" * 70)
    print("SHARED GENERATION TEST")
    print("=" * 70)
    print()

    question = "How does TCP slow start work?"

    print("Retrieving documents...")
    documents = retrieve_documents(question, k=3)

    print(f"Retrieved documents: {len(documents)}")
    print()

    print("Generating answer...")
    answer = generate_answer(
        question,
        documents,
    )

    print()
    print("=" * 70)
    print("GENERATED ANSWER")
    print("=" * 70)
    print(answer)

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    assert isinstance(answer, str)
    assert answer.strip()

    print("Answer is a non-empty string: PASS")
    print("Shared generation function: PASS")
    print()
    print("Shared generation test passed.")


if __name__ == "__main__":
    main()