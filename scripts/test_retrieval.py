from app.vector_store.chroma import create_vectorstore


TOP_K = 3


# Retrieval metrics are meaningful only for questions whose answers
# are supported by the indexed documents.
#
# Unsupported and out-of-scope questions are still displayed as
# diagnostics, but they are excluded from Hit@1, Hit@3 and MRR.
SUPPORTED_CATEGORIES = {
    "direct",
    "paraphrased",
    "vague",
    "difficult",
}


EVALUATION_DATA = [
    # ---------------------------------------------------------
    # Direct in-scope questions
    # ---------------------------------------------------------
    {
        "id": "direct_1",
        "category": "direct",
        "question": "How does TCP slow start work?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_3",
        ],
    },
    {
        "id": "direct_2",
        "category": "direct",
        "question": "What is TCP Tahoe?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_4",
        ],
    },
    {
        "id": "direct_3",
        "category": "direct",
        "question": "What is TCP Reno?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_5",
        ],
    },
    {
        "id": "direct_4",
        "category": "direct",
        "question": "What is congestion avoidance?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_4",
            "congestion_control.pdf::chunk_9",
        ],
    },
    {
        "id": "direct_5",
        "category": "direct",
        "question": "What is additive increase multiplicative decrease?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_5",
        ],
    },
    {
        "id": "direct_6",
        "category": "direct",
        "question": "What happens when TCP detects packet loss?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_4",
            "congestion_control.pdf::chunk_9",
        ],
    },
    {
        "id": "direct_7",
        "category": "direct",
        "question": "What is explicit congestion notification?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_7",
        ],
    },

    # ---------------------------------------------------------
    # Paraphrased questions
    # ---------------------------------------------------------
    {
        "id": "paraphrase_1",
        "category": "paraphrased",
        "question": "How does TCP initially increase its congestion window?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_3",
        ],
    },
    {
        "id": "paraphrase_2",
        "category": "paraphrased",
        "question": "How does TCP detect and respond to congestion?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_4",
            "congestion_control.pdf::chunk_9",
        ],
    },
    {
        "id": "paraphrase_3",
        "category": "paraphrased",
        "question": "How does TCP increase its sending rate without causing too much congestion?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_4",
            "congestion_control.pdf::chunk_5",
        ],
    },

    # ---------------------------------------------------------
    # Vague / underspecified questions
    # ---------------------------------------------------------
    {
        "id": "vague_1",
        "category": "vague",
        "question": "What happens when the network gets congested?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_2",
            "congestion_control.pdf::chunk_4",
        ],
    },
    {
        "id": "vague_2",
        "category": "vague",
        "question": "How does TCP deal with this problem?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_2",
            "congestion_control.pdf::chunk_4",
        ],
    },
    {
        "id": "vague_3",
        "category": "vague",
        "question": "What does TCP do when things go wrong?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_4",
            "congestion_control.pdf::chunk_9",
        ],
    },

    # ---------------------------------------------------------
    # Difficult / integrated questions
    # ---------------------------------------------------------
    {
        "id": "difficult_1",
        "category": "difficult",
        "question": "How does TCP change its congestion window during slow start and congestion avoidance?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_3",
            "congestion_control.pdf::chunk_4",
        ],
    },
    {
        "id": "difficult_2",
        "category": "difficult",
        "question": "What are the main phases of TCP congestion control?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_2",
            "congestion_control.pdf::chunk_3",
            "congestion_control.pdf::chunk_4",
        ],
    },
    {
        "id": "difficult_3",
        "category": "difficult",
        "question": "How are TCP Tahoe and TCP Reno different when packet loss is detected?",
        "relevant_ids": [
            "congestion_control.pdf::chunk_4",
            "congestion_control.pdf::chunk_5",
        ],
    },

    # ---------------------------------------------------------
    # Out-of-scope questions
    # ---------------------------------------------------------
    {
        "id": "out_of_scope_1",
        "category": "out_of_scope",
        "question": "What is the capital of France?",
        "relevant_ids": [],
    },
    {
        "id": "out_of_scope_2",
        "category": "out_of_scope",
        "question": "Explain how a convolutional neural network works.",
        "relevant_ids": [],
    },
    {
        "id": "out_of_scope_3",
        "category": "out_of_scope",
        "question": "What is the difference between Python and Java?",
        "relevant_ids": [],
    },

    # ---------------------------------------------------------
    # Related to the topic but unsupported by current documents
    # ---------------------------------------------------------
    {
        "id": "unsupported_1",
        "category": "related_unsupported",
        "question": "How does TCP CUBIC work?",
        "relevant_ids": [],
    },
    {
        "id": "unsupported_2",
        "category": "related_unsupported",
        "question": "What is TCP BBR?",
        "relevant_ids": [],
    },
    {
        "id": "unsupported_3",
        "category": "related_unsupported",
        "question": "How does TCP New Reno improve on TCP Reno?",
        "relevant_ids": [],
    },
]


def calculate_metrics(results):
    if not results:
        return {
            "hit_at_1": 0.0,
            "hit_at_3": 0.0,
            "mrr": 0.0,
        }

    total = len(results)

    hit_at_1 = sum(
        result["hit_at_1"]
        for result in results
    ) / total

    hit_at_3 = sum(
        result["hit_at_3"]
        for result in results
    ) / total

    reciprocal_ranks = [
        result["reciprocal_rank"]
        for result in results
    ]

    mrr = sum(reciprocal_ranks) / total

    return {
        "hit_at_1": hit_at_1,
        "hit_at_3": hit_at_3,
        "mrr": mrr,
    }


def main():
    print("=" * 80)
    print("BASELINE RETRIEVAL EVALUATION")
    print("=" * 80)
    print()

    vectorstore = create_vectorstore()

    results = []
    all_results = []

    for index, item in enumerate(EVALUATION_DATA, start=1):
        question = item["question"]
        relevant_ids = set(item["relevant_ids"])

        documents = vectorstore.similarity_search(
            question,
            k=TOP_K,
        )

        retrieved_ids = [
            f"{document.metadata.get('source')}::"
            f"chunk_{document.metadata.get('chunk_index')}"
            for document in documents
        ]

        hit_at_1 = bool(
            retrieved_ids
            and relevant_ids
            and retrieved_ids[0] in relevant_ids
        )

        relevant_ranks = [
            rank
            for rank, document_id in enumerate(
                retrieved_ids,
                start=1,
            )
            if document_id in relevant_ids
        ]

        if relevant_ranks:
            reciprocal_rank = 1 / relevant_ranks[0]
        else:
            reciprocal_rank = 0.0

        hit_at_3 = bool(
            relevant_ids.intersection(retrieved_ids)
        )

        is_supported = item["category"] in SUPPORTED_CATEGORIES

        result = {
            "id": item["id"],
            "category": item["category"],
            "question": question,
            "retrieved_ids": retrieved_ids,
            "evaluable": is_supported,
            "hit_at_1": int(hit_at_1) if is_supported else None,
            "hit_at_3": int(hit_at_3) if is_supported else None,
            "reciprocal_rank": (
                reciprocal_rank
                if is_supported
                else None
            ),
        }

        all_results.append(result)

        if is_supported:
            results.append(result)

        print(f"{index}. [{item['category']}]")
        print(f"   Question: {question}")
        print()

        for rank, document_id in enumerate(
            retrieved_ids,
            start=1,
        ):
            marker = (
                " <-- relevant"
                if document_id in relevant_ids
                else ""
            )
            print(
                f"   Rank {rank}: "
                f"{document_id}{marker}"
            )

        print()

        if is_supported:
            print(f"   Hit@1: {hit_at_1}")
            print(f"   Hit@3: {hit_at_3}")
            print(
                f"   Reciprocal Rank: "
                f"{reciprocal_rank:.4f}"
            )
        else:
            print(
                "   Retrieval metrics: EXCLUDED "
                "(question is unsupported/out-of-scope)"
            )

        print()
        print("-" * 80)

    metrics = calculate_metrics(results)

    print()
    print("=" * 80)
    print("SUPPORTED RETRIEVAL RESULTS")
    print("=" * 80)

    print(
        f"Questions evaluated: {len(results)}"
    )
    print(
        f"Hit@1:              "
        f"{metrics['hit_at_1'] * 100:.2f}%"
    )
    print(
        f"Hit@3:              "
        f"{metrics['hit_at_3'] * 100:.2f}%"
    )
    print(
        f"MRR:                "
        f"{metrics['mrr']:.4f}"
    )

    excluded_count = (
        len(EVALUATION_DATA) - len(results)
    )

    print()
    print(
        f"Excluded from retrieval metrics: "
        f"{excluded_count} "
        "(unsupported/out-of-scope)"
    )

    print(
        "These questions are evaluated separately "
        "for answerability and refusal behavior."
    )

    print()
    print("=" * 80)
    print("RESULTS BY CATEGORY")
    print("=" * 80)

    categories = sorted(
        set(result["category"] for result in results)
    )

    for category in categories:
        category_results = [
            result
            for result in results
            if result["category"] == category
        ]

        category_metrics = calculate_metrics(
            category_results
        )

        print(f"\n{category}")
        print(
            f"  Questions: "
            f"{len(category_results)}"
        )
        print(
            f"  Hit@1: "
            f"{category_metrics['hit_at_1'] * 100:.2f}%"
        )
        print(
            f"  Hit@3: "
            f"{category_metrics['hit_at_3'] * 100:.2f}%"
        )
        print(
            f"  MRR: "
            f"{category_metrics['mrr']:.4f}"
        )

    print()
    print("Excluded categories:")
    print("  out_of_scope")
    print("  related_unsupported")
    print(
        "  These are intentionally excluded from "
        "retrieval metrics because their answers "
        "are not present in the indexed documents."
    )


if __name__ == "__main__":
    main()