from pydantic import BaseModel, Field

from app.llm.model import create_llm


class QueryRewrite(BaseModel):
    search_query: str = Field(
        description=(
            "A rewritten search query optimized for retrieving "
            "documents that can answer the original question."
        )
    )
    reason: str = Field(
        description=(
            "Brief explanation of why this query should retrieve "
            "better evidence."
        )
    )


REWRITE_PROMPT = """
You are improving a search query for a student knowledge assistant.

The system retrieved documents that were not sufficient to answer
the user's original question.

Rewrite the search query so that a vector database is more likely
to retrieve documents containing the specific information needed.

Rules:
- Preserve the meaning of the original question.
- Do not answer the question.
- Produce a search query, not a full sentence answer.
- Use specific technical terminology when appropriate.
- Focus on the information that was missing from the previous retrieval.
- Do not add facts that are not implied by the original question
  or grading feedback.
- Make the rewritten query meaningfully different when possible.

Original question:
{question}

Previous search query:
{search_query}

Grader feedback:
{grade_reason}
"""


def main():
    print("=" * 70)
    print("QUERY REWRITE TEST")
    print("=" * 70)
    print()

    llm = create_llm()

    structured_llm = llm.with_structured_output(
        QueryRewrite
    )

    question = (
        "How does TCP work when congestion happens?"
    )

    search_query = question

    grade_reason = (
        "The retrieved documents discuss TCP generally, "
        "but they do not provide enough specific information "
        "about how TCP responds to network congestion."
    )

    prompt = REWRITE_PROMPT.format(
        question=question,
        search_query=search_query,
        grade_reason=grade_reason,
    )

    result = structured_llm.invoke(prompt)

    print("Original question:")
    print(question)
    print()

    print("Previous search query:")
    print(search_query)
    print()

    print("Rewritten search query:")
    print(result.search_query)
    print()

    print("Reason:")
    print(result.reason)
    print()

    assert isinstance(
        result.search_query,
        str,
    )

    assert result.search_query.strip()

    assert isinstance(
        result.reason,
        str,
    )

    assert result.reason.strip()

    print("Search query validated: PASS")
    print("Rewrite reason validated: PASS")
    print()
    print("Query rewrite test passed.")


if __name__ == "__main__":
    main()