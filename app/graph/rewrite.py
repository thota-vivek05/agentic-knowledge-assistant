from pydantic import BaseModel, Field

from app.graph.state import GraphState
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


def rewrite_query(state: GraphState) -> dict:
    """
    Rewrite the current search query using the original question
    and grader feedback.
    """

    llm = create_llm()

    structured_llm = llm.with_structured_output(
        QueryRewrite
    )

    prompt = REWRITE_PROMPT.format(
        question=state["question"],
        search_query=state["search_query"],
        grade_reason=state["grade_reason"],
    )

    result = structured_llm.invoke(prompt)

    return {
        "search_query": result.search_query,
        "rewrite_count": state["rewrite_count"] + 1,
    }