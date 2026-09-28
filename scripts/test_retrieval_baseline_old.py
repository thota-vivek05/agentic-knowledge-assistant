from app.vector_store.chroma import create_vectorstore


TOP_K = 3


EVALUATION_DATA = [
    {
        "question": "How does TCP slow start work?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_3",
        ],
    },
    {
        "question": "What is TCP Tahoe?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_4",
        ],
    },
    {
        "question": "What is TCP Reno?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_5",
        ],
    },
    {
        "question": "What is congestion avoidance?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_4",
            "congestion_control.pdf::chunk_9",
        ],
    },
    {
        "question": "What is additive increase multiplicative decrease?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_5",
        ],
    },
    {
        "question": "What happens when TCP detects packet loss?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_4",
            "congestion_control.pdf::chunk_9",
        ],
    },
    {
        "question": "What is explicit congestion notification?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_7",
        ],
    },
]


def get_document_id(document) -> str:
    """
    Convert a retrieved LangChain Document into the stable
    document ID used by Chroma.

    The ID is reconstructed from source + chunk_index because
    similarity_search() returns Documents rather than IDs.
    """

    source = document.metadata["source"]
    chunk_index = document.metadata["chunk_index"]

    return f"{source}::chunk_{chunk_index}"


def reciprocal_rank(
    retrieved_ids: list[str],
    relevant_ids: set[str],
) -> float:
    """
    Calculate Reciprocal Rank.

    If the first relevant result is at rank:
        1 -> 1.0
        2 -> 0.5
        3 -> 0.333...
        etc.

    If no relevant result is found:
        0.0
    """

    for rank, document_id in enumerate(
        retrieved_ids,
        start=1,
    ):

        if document_id in relevant_ids:
            return 1.0 / rank

    return 0.0


def main():

    vectorstore = create_vectorstore()

    hit_at_1_count = 0
    hit_at_3_count = 0

    reciprocal_ranks = []

    print("=" * 70)
    print("RETRIEVAL EVALUATION")
    print("=" * 70)
    print()

    for index, item in enumerate(
        EVALUATION_DATA,
        start=1,
    ):

        question = item["question"]

        relevant_ids = set(
            item["relevant_ids"]
        )

        # -----------------------------------------------------
        # Retrieve top-k documents
        # -----------------------------------------------------

        results = vectorstore.similarity_search(
            question,
            k=TOP_K,
        )

        retrieved_ids = [
            get_document_id(document)
            for document in results
        ]

        # -----------------------------------------------------
        # Calculate Hit@1
        # -----------------------------------------------------

        hit_at_1 = (
            len(relevant_ids.intersection(
                set(retrieved_ids[:1])
            )) > 0
        )

        if hit_at_1:
            hit_at_1_count += 1

        # -----------------------------------------------------
        # Calculate Hit@3
        # -----------------------------------------------------

        hit_at_3 = (
            len(relevant_ids.intersection(
                set(retrieved_ids[:TOP_K])
            )) > 0
        )

        if hit_at_3:
            hit_at_3_count += 1

        # -----------------------------------------------------
        # Calculate MRR
        # -----------------------------------------------------

        rr = reciprocal_rank(
            retrieved_ids,
            relevant_ids,
        )

        reciprocal_ranks.append(rr)

        # -----------------------------------------------------
        # Print query information
        # -----------------------------------------------------

        print(f"Query {index}: {question}")
        print()

        print("Expected relevant IDs:")
        for document_id in sorted(relevant_ids):
            print(f"  {document_id}")

        print()

        print("Retrieved:")
        for rank, document in enumerate(
            results,
            start=1,
        ):

            document_id = retrieved_ids[rank - 1]

            is_relevant = (
                document_id in relevant_ids
            )

            marker = " <-- RELEVANT" if is_relevant else ""

            print(
                f"  {rank}. {document_id}{marker}"
            )

        print()

        print(
            f"Hit@1: {'PASS' if hit_at_1 else 'FAIL'}"
        )

        print(
            f"Hit@{TOP_K}: "
            f"{'PASS' if hit_at_3 else 'FAIL'}"
        )

        print(
            f"Reciprocal Rank: {rr:.3f}"
        )

        print("-" * 70)
        print()

    # ---------------------------------------------------------
    # Calculate final metrics
    # ---------------------------------------------------------

    total_queries = len(EVALUATION_DATA)

    hit_at_1 = (
        hit_at_1_count / total_queries
    )

    hit_at_3 = (
        hit_at_3_count / total_queries
    )

    mrr = (
        sum(reciprocal_ranks)
        / total_queries
    )

    # ---------------------------------------------------------
    # Print summary
    # ---------------------------------------------------------

    print("=" * 70)
    print("FINAL RETRIEVAL RESULTS")
    print("=" * 70)
    print()

    print(
        f"Queries evaluated: {total_queries}"
    )

    print(
        f"Hit@1: {hit_at_1 * 100:.2f}%"
    )

    print(
        f"Hit@{TOP_K}: {hit_at_3 * 100:.2f}%"
    )

    print(
        f"MRR: {mrr:.4f}"
    )

    print()

    print(
        "Metric definitions:"
    )

    print(
        "  Hit@k  = whether at least one manually labeled "
        "relevant chunk appears in the top-k results."
    )

    print(
        "  MRR    = average reciprocal rank of the first "
        "relevant result."
    )

    print()

    print(
        "Note: this is a manually constructed evaluation set "
        "for the congestion-control document. It evaluates "
        "retrieval ranking, not answer-generation quality."
    )


if __name__ == "__main__":
    main()