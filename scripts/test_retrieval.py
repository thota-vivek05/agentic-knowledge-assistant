from app.vector_store.chroma import create_vectorstore


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


TOP_K = 3


def calculate_recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: list[str],
) -> bool:
    """
    Return True if at least one relevant document
    appears in the retrieved top-k results.
    """

    return any(
        document_id in relevant_ids
        for document_id in retrieved_ids
    )


vectorstore = create_vectorstore()


print("=" * 80)
print("RETRIEVAL EVALUATION")
print("=" * 80)

print(f"\nEvaluation queries: {len(EVALUATION_DATA)}")
print(f"Top K: {TOP_K}")


recall_at_1_results = []
recall_at_3_results = []


for index, item in enumerate(EVALUATION_DATA, start=1):

    question = item["question"]
    relevant_ids = item["relevant_ids"]

    results = vectorstore.similarity_search(
        question,
        k=TOP_K,
    )

    retrieved_ids = [
        (
            f"{result.metadata['source']}"
            f"::chunk_{result.metadata['chunk_index']}"
        )
        for result in results
    ]

    recall_at_1 = calculate_recall_at_k(
        retrieved_ids[:1],
        relevant_ids,
    )

    recall_at_3 = calculate_recall_at_k(
        retrieved_ids[:3],
        relevant_ids,
    )

    recall_at_1_results.append(recall_at_1)
    recall_at_3_results.append(recall_at_3)

    print("\n" + "=" * 80)
    print(f"QUERY {index}")
    print("=" * 80)

    print(f"\nQuestion:")
    print(question)

    print("\nExpected relevant chunks:")
    for document_id in relevant_ids:
        print(f"  {document_id}")

    print("\nRetrieved chunks:")

    for rank, document_id in enumerate(
        retrieved_ids,
        start=1,
    ):
        status = (
            "RELEVANT"
            if document_id in relevant_ids
            else "not relevant"
        )

        print(
            f"  {rank}. {document_id} "
            f"[{status}]"
        )

    print(
        f"\nRecall@1: "
        f"{'PASS' if recall_at_1 else 'FAIL'}"
    )

    print(
        f"Recall@3: "
        f"{'PASS' if recall_at_3 else 'FAIL'}"
    )


recall_at_1 = (
    sum(recall_at_1_results)
    / len(recall_at_1_results)
    * 100
)

recall_at_3 = (
    sum(recall_at_3_results)
    / len(recall_at_3_results)
    * 100
)


print("\n" + "=" * 80)
print("FINAL RESULTS")
print("=" * 80)

print(
    f"\nRecall@1: "
    f"{recall_at_1:.2f}%"
)

print(
    f"Recall@3: "
    f"{recall_at_3:.2f}%"
)