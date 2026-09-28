from app.rag.chain import answer_question
from app.rag.context import format_sources


def main():

    question = "How does TCP slow start work?"

    print("=" * 70)
    print("BASELINE RAG TEST")
    print("=" * 70)
    print()

    print(f"Question: {question}")
    print()

    result = answer_question(
        question,
        k=3,
    )

    print("=" * 70)
    print("ANSWER")
    print("=" * 70)
    print()

    print(result["answer"])

    if result["documents"]:

        print()
        print("=" * 70)
        print("SOURCES")
        print("=" * 70)

        for index, source in enumerate(
            format_sources(result["documents"]),
            start=1,
        ):
            print(
                f"{index}. {source}"
            )


if __name__ == "__main__":
    main()