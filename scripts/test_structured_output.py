from pydantic import BaseModel, Field

from app.llm.model import create_llm


class TestDecision(BaseModel):
    decision: bool = Field(
        description="Whether the provided information is relevant."
    )
    reason: str = Field(
        description="Short explanation for the decision."
    )


def main():
    print("=" * 70)
    print("GEMINI STRUCTURED OUTPUT TEST")
    print("=" * 70)
    print()

    llm = create_llm()

    structured_llm = llm.with_structured_output(TestDecision)

    question = """
    Is TCP slow start related to congestion control?

    Answer using the following information:

    TCP slow start is one of the mechanisms used by TCP
    for congestion control.
    """

    print("Sending structured-output request...")
    print()

    result = structured_llm.invoke(question)

    print("Result:")
    print(result)
    print()

    print(f"Type: {type(result)}")
    print()

    assert isinstance(result, TestDecision)
    assert isinstance(result.decision, bool)
    assert isinstance(result.reason, str)
    assert result.reason.strip()

    print("Pydantic object returned: PASS")
    print("Boolean field validated: PASS")
    print("Reason field validated: PASS")
    print()
    print("Structured output test passed.")


if __name__ == "__main__":
    main()