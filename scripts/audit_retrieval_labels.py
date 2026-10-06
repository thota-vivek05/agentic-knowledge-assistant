from app.rag.chain import retrieve_documents
from scripts.evaluation_data import EVALUATION_DATA


def main():
    for index, case in enumerate(EVALUATION_DATA, start=1):
        question = case["question"]
        expected_ids = set(case.get("relevant_ids", []))

        documents = retrieve_documents(question, k=5)

        print("\n" + "=" * 80)
        print(f"{index}. {question}")
        print(f"Category: {case['category']}")
        print(f"Expected IDs: {sorted(expected_ids)}")

        print("\nRetrieved:")
        for rank, document in enumerate(documents, start=1):
            metadata = document.metadata

            chunk_id = (
                f"{metadata['source']}::"
                f"chunk_{metadata['chunk_index']}"
            )

            print(
                f"{rank}. {chunk_id} "
                f"(pages {metadata.get('start_page')}-"
                f"{metadata.get('end_page')})"
            )

            preview = document.page_content[:250].replace("\n", " ")
            print(f"   {preview}...")


if __name__ == "__main__":
    main()