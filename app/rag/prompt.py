from langchain_core.prompts import ChatPromptTemplate


NOT_FOUND_MESSAGE = (
    "I don't have enough information in the provided documents "
    "to answer that question."
)


RAG_SYSTEM_PROMPT = """
You are a knowledge assistant for students.

Answer the user's question using only the provided context.

Rules:
1. Use only information contained in the context.
2. Do not use outside knowledge to answer the question.
3. If the context does not contain enough information to answer
   the question, reply with exactly:

   {not_found_message}

4. Do not invent facts.
5. Do not write source names, page numbers, or chunk numbers
   yourself. Sources are added separately by the application.
6. Keep the answer clear and concise.

Context:
{context}
"""


def create_rag_prompt() -> ChatPromptTemplate:
    """
    Create the prompt used by the baseline RAG pipeline.
    """

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                RAG_SYSTEM_PROMPT,
            ),
            (
                "human",
                "{question}",
            ),
        ]
    ).partial(
        not_found_message=NOT_FOUND_MESSAGE
    )