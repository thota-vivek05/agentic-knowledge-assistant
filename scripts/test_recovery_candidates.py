from app.graph.grader import grade_documents, format_documents
from app.rag.chain import retrieve_documents

from scripts.recovery_candidates import RECOVERY_CANDIDATES


def main():
    print("=" * 70)
    print("RECOVERY CANDIDATE DIAGNOSTIC")
    print("=" * 70)
    print()

    for index, candidate in enumerate(
        RECOVERY_CANDIDATES,
        start=1,
    ):
        question = candidate["question"]
        target_concept = candidate["target_concept"]

        print("=" * 70)
        print(f"[{index}/{len(RECOVERY_CANDIDATES)}]")
        print("=" * 70)

        print(f"Question:")
        print(f"  {question}")

        print()
        print(f"Target concept:")
        print(f"  {target_concept}")

        documents = retrieve_documents(
            question,
            k=3,
        )

        print()
        print("Retrieved chunks:")

        for document in documents:
            metadata = document.metadata

            print(
                f"  chunk={metadata.get('chunk_index')} "
                f"pages={metadata.get('start_page')}-"
                f"{metadata.get('end_page')}"
            )

        state = {
            "question": question,
            "search_query": question,
            "documents": documents,
            "relevant_documents": [],
            "sufficient": False,
            "grade_reason": "",
            "rewrite_count": 0,
            "answer": "",
            "answered": False,
        }

        grade_result = grade_documents(state)

        print()
        print("Grader result:")
        print(f"  sufficient: {grade_result['sufficient']}")
        print(f"  relevant chunks: {len(grade_result['relevant_documents'])}")
        print(f"  reason: {grade_result['grade_reason']}")

        print()


if __name__ == "__main__":
    main()