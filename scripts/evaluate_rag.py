from collections import defaultdict

from app.graph.workflow import build_retry_graph
from app.rag.chain import answer_question
from app.rag.prompt import NOT_FOUND_MESSAGE

from scripts.evaluation_data import EVALUATION_DATA


def evaluate_baseline(question: str, expected_answered: bool) -> dict:
    result = answer_question(question)

    answered = result["answered"]

    return {
        "answered": answered,
        "correct": answered == expected_answered,
    }


def evaluate_corrective(
    graph,
    question: str,
    expected_answered: bool,
) -> dict:
    initial_state = {
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

    result = graph.invoke(initial_state)

    answered = result["answered"]

    # Explicitly verify that an unanswered result uses
    # the deterministic fallback message.
    if not answered:
        assert result["answer"] == NOT_FOUND_MESSAGE

    return {
        "answered": answered,
        "correct": answered == expected_answered,
        "rewrite_count": result["rewrite_count"],
    }


def calculate_summary(results: list[dict]) -> dict:
    total = len(results)

    baseline_correct = sum(
        result["baseline_correct"]
        for result in results
    )

    corrective_correct = sum(
        result["corrective_correct"]
        for result in results
    )

    supported = [
        result
        for result in results
        if result["expected_answered"]
    ]

    unsupported = [
        result
        for result in results
        if not result["expected_answered"]
    ]

    baseline_supported_answered = sum(
        result["baseline_answered"]
        for result in supported
    )

    corrective_supported_answered = sum(
        result["corrective_answered"]
        for result in supported
    )

    baseline_refusals = sum(
        not result["baseline_answered"]
        for result in unsupported
    )

    corrective_refusals = sum(
        not result["corrective_answered"]
        for result in unsupported
    )

    average_rewrites = (
        sum(result["corrective_rewrites"] for result in results)
        / total
    )

    return {
        "total": total,
        "baseline_accuracy": baseline_correct / total,
        "corrective_accuracy": corrective_correct / total,
        "baseline_supported_answer_rate": (
            baseline_supported_answered / len(supported)
        ),
        "corrective_supported_answer_rate": (
            corrective_supported_answered / len(supported)
        ),
        "baseline_unsupported_refusal_rate": (
            baseline_refusals / len(unsupported)
        ),
        "corrective_unsupported_refusal_rate": (
            corrective_refusals / len(unsupported)
        ),
        "average_corrective_rewrites": average_rewrites,
    }


def print_summary(summary: dict):
    print()
    print("=" * 70)
    print("OVERALL RESULTS")
    print("=" * 70)

    print(f"Total questions: {summary['total']}")

    print()
    print(
        f"Baseline answerability accuracy: "
        f"{summary['baseline_accuracy']:.2%}"
    )

    print(
        f"Corrective answerability accuracy: "
        f"{summary['corrective_accuracy']:.2%}"
    )

    print()
    print(
        f"Baseline supported-question answer rate: "
        f"{summary['baseline_supported_answer_rate']:.2%}"
    )

    print(
        f"Corrective supported-question answer rate: "
        f"{summary['corrective_supported_answer_rate']:.2%}"
    )

    print()
    print(
        f"Baseline unsupported-question refusal rate: "
        f"{summary['baseline_unsupported_refusal_rate']:.2%}"
    )

    print(
        f"Corrective unsupported-question refusal rate: "
        f"{summary['corrective_unsupported_refusal_rate']:.2%}"
    )

    print()
    print(
        f"Average corrective rewrites: "
        f"{summary['average_corrective_rewrites']:.2f}"
    )


def print_category_results(results: list[dict]):
    grouped = defaultdict(list)

    for result in results:
        grouped[result["category"]].append(result)

    print()
    print("=" * 70)
    print("RESULTS BY CATEGORY")
    print("=" * 70)

    for category, category_results in grouped.items():
        baseline_correct = sum(
            result["baseline_correct"]
            for result in category_results
        )

        corrective_correct = sum(
            result["corrective_correct"]
            for result in category_results
        )

        count = len(category_results)

        print()
        print(f"{category}:")
        print(
            f"  Baseline:   "
            f"{baseline_correct}/{count} "
            f"({baseline_correct / count:.2%})"
        )
        print(
            f"  Corrective: "
            f"{corrective_correct}/{count} "
            f"({corrective_correct / count:.2%})"
        )


def main():
    print("=" * 70)
    print("BASELINE VS CORRECTIVE RAG EVALUATION")
    print("=" * 70)
    print()

    graph = build_retry_graph()

    results = []

    for index, item in enumerate(EVALUATION_DATA, start=1):
        question = item["question"]
        category = item["category"]
        expected_answered = item["expected_answered"]

        print(
            f"[{index:02d}/{len(EVALUATION_DATA)}] "
            f"{category}: {question}"
        )

        baseline = evaluate_baseline(
            question,
            expected_answered,
        )

        corrective = evaluate_corrective(
            graph,
            question,
            expected_answered,
        )

        result = {
            "question": question,
            "category": category,
            "expected_answered": expected_answered,
            "baseline_answered": baseline["answered"],
            "baseline_correct": baseline["correct"],
            "corrective_answered": corrective["answered"],
            "corrective_correct": corrective["correct"],
            "corrective_rewrites": corrective["rewrite_count"],
        }

        results.append(result)

        print(
            f"  Baseline: "
            f"answered={baseline['answered']} "
            f"correct={baseline['correct']}"
        )

        print(
            f"  Corrective: "
            f"answered={corrective['answered']} "
            f"correct={corrective['correct']} "
            f"rewrites={corrective['rewrite_count']}"
        )

        print()

    summary = calculate_summary(results)

    print_summary(summary)
    print_category_results(results)

    print()
    print("=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()