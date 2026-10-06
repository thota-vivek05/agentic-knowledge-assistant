from collections import Counter

from scripts.evaluation_data import EVALUATION_DATA


EXPECTED_CATEGORIES = {
    "direct",
    "paraphrased",
    "vague",
    "difficult",
    "out_of_scope",
    "related_unsupported",
}


def main():
    print("=" * 70)
    print("ANSWER-LEVEL EVALUATION DATASET TEST")
    print("=" * 70)
    print()

    print(f"Total questions: {len(EVALUATION_DATA)}")

    assert len(EVALUATION_DATA) == 22

    categories = Counter(
        item["category"]
        for item in EVALUATION_DATA
    )

    print()
    print("Questions by category:")

    for category, count in categories.items():
        print(f"  {category}: {count}")

    print()

    assert set(categories.keys()) == EXPECTED_CATEGORIES

    # Every question must have the required fields.
    for item in EVALUATION_DATA:
        assert "question" in item
        assert "category" in item
        assert "expected_answered" in item

        assert isinstance(item["question"], str)
        assert item["question"].strip()

        assert item["category"] in EXPECTED_CATEGORIES
        assert isinstance(item["expected_answered"], bool)

    # Supported categories should be answerable.
    for item in EVALUATION_DATA:
        if item["category"] in {
            "direct",
            "paraphrased",
            "vague",
            "difficult",
        }:
            assert item["expected_answered"] is True

    # Unsupported categories should be unanswerable.
    for item in EVALUATION_DATA:
        if item["category"] in {
            "out_of_scope",
            "related_unsupported",
        }:
            assert item["expected_answered"] is False

    print("Required fields: PASS")
    print("Category labels: PASS")
    print("Answerability labels: PASS")

    print()
    print("Answer-level evaluation dataset test passed.")


if __name__ == "__main__":
    main()