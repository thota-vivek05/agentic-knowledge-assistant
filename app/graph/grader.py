from pydantic import BaseModel, Field

from app.llm.model import create_llm
from app.graph.state import GraphState


class ChunkGrade(BaseModel):
    chunk_index: int = Field(
        description="The chunk_index from the retrieved document."
    )
    relevant: bool = Field(
        description=(
            "Whether this chunk contains substantive information "
            "directly needed to answer the user's original question."
        )
    )
    reason: str = Field(
        description="Brief explanation for the relevance decision."
    )


class RetrievalGrade(BaseModel):
    grades: list[ChunkGrade] = Field(
        description=(
            "Relevance evaluation for every retrieved chunk. "
            "Every retrieved chunk must be evaluated."
        )
    )
    sufficient: bool = Field(
        description=(
            "Whether the relevant chunks together contain enough "
            "information to answer the original question accurately "
            "without relying on outside knowledge."
        )
    )
    reason: str = Field(
        description=(
            "Brief explanation of why the available evidence "
            "is or is not sufficient."
        )
    )


GRADER_PROMPT = """
You are evaluating retrieved documents for a student knowledge assistant.

Your job is to determine whether the retrieved documents contain
enough information to answer the user's ORIGINAL question.

Important distinctions:

- A chunk can be relevant without the overall evidence being sufficient.
- A chunk is relevant only if its content directly contributes
  substantive information needed to answer the original question.
- Do NOT mark a chunk relevant merely because:
  - it discusses the same broad topic,
  - it mentions TCP,
  - it discusses congestion control generally, or
  - it provides unrelated background information.
- For example, if the question asks specifically about TCP slow start,
  a chunk should be marked relevant only if it contains information
  about slow start or a mechanism directly necessary to explain it.
- The evidence is sufficient only when the relevant chunks together
  contain enough information to answer the original question accurately.
- Do not use outside knowledge.
- Evaluate EVERY retrieved chunk.
- Return the chunk_index exactly as provided.

The `sufficient` field must be false when the retrieved documents
do not contain enough information to answer the original question
without relying on outside knowledge.

Original question:
{question}

Retrieved documents:

{documents}
"""


def format_documents(documents) -> str:
    """
    Format retrieved documents for the grading prompt.
    """

    parts = []

    for document in documents:
        metadata = document.metadata

        chunk_index = metadata.get("chunk_index", "unknown")
        source = metadata.get("source", "Unknown source")
        start_page = metadata.get("start_page", "?")
        end_page = metadata.get("end_page", "?")

        parts.append(
            f"""
[Chunk {chunk_index}]
Source: {source}
Pages: {start_page}-{end_page}

{document.page_content}
""".strip()
        )

    return "\n\n".join(parts)


def grade_documents(state: GraphState) -> dict:
    """
    Grade all retrieved documents in a single LLM call.

    Returns:
        relevant_documents: Documents judged directly relevant.
        sufficient: Whether the evidence is sufficient to answer.
        grade_reason: Explanation for the overall grading decision.
    """

    llm = create_llm()

    structured_llm = llm.with_structured_output(
        RetrievalGrade
    )

    documents_text = format_documents(
        state["documents"]
    )

    prompt = GRADER_PROMPT.format(
        question=state["question"],
        documents=documents_text,
    )

    result = structured_llm.invoke(prompt)

    relevant_chunk_indices = {
        grade.chunk_index
        for grade in result.grades
        if grade.relevant
    }

    relevant_documents = [
        document
        for document in state["documents"]
        if document.metadata.get("chunk_index")
        in relevant_chunk_indices
    ]

    return {
        "relevant_documents": relevant_documents,
        "sufficient": result.sufficient,
        "grade_reason": result.reason,
    }