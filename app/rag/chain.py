from functools import lru_cache

from langchain_core.output_parsers import StrOutputParser

from app.llm.model import create_llm
from app.rag.context import format_context
from app.rag.prompt import (
    NOT_FOUND_MESSAGE,
    create_rag_prompt,
)
from app.vector_store.chroma import create_vectorstore


@lru_cache(maxsize=1)
def get_vectorstore():
    """
    Create and cache the ChromaDB vector store.
    """

    return create_vectorstore()


@lru_cache(maxsize=1)
def get_rag_chain():
    """
    Create and cache the baseline RAG generation chain.
    """

    llm = create_llm()
    prompt = create_rag_prompt()

    return (
        prompt
        | llm
        | StrOutputParser()
    )


def retrieve_documents(
    question: str,
    k: int = 3,
):
    """
    Retrieve the top-k relevant documents from ChromaDB.
    """

    vectorstore = get_vectorstore()

    return vectorstore.similarity_search(
        question,
        k=k,
    )


def answer_question(
    question: str,
    k: int = 3,
) -> dict:
    """
    Retrieve relevant documents and generate a grounded answer.

    Returns:
        answer:
            Generated answer.

        answered:
            True if the question could be answered from the
            provided documents.

        documents:
            Retrieved documents when the question was answered.
            Empty when the model refused because the context
            was insufficient.
    """

    documents = retrieve_documents(
        question,
        k=k,
    )

    context = format_context(
        documents
    )

    chain = get_rag_chain()

    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    answered = NOT_FOUND_MESSAGE not in answer

    return {
        "answer": answer,
        "answered": answered,
        "documents": documents if answered else [],
    }