from functools import lru_cache

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from app.llm.model import create_llm
from app.rag.context import format_context
from app.rag.prompt import NOT_FOUND_MESSAGE, create_rag_prompt
from app.vector_store.chroma import create_vectorstore


@lru_cache(maxsize=1)
def get_vectorstore():
    return create_vectorstore()


@lru_cache(maxsize=1)
def get_rag_chain():
    llm = create_llm()
    prompt = create_rag_prompt()

    return prompt | llm | StrOutputParser()


def retrieve_documents(question: str, k: int = 3) -> list[Document]:
    vectorstore = get_vectorstore()

    return vectorstore.similarity_search(
        question,
        k=k,
    )


def generate_answer(
    question: str,
    documents: list[Document],
) -> str:
    """
    Generate an answer using only the supplied documents.

    Retrieval and grading are intentionally handled outside this
    function so the same generation logic can be reused by both
    baseline RAG and corrective RAG.
    """
    context = format_context(documents)

    chain = get_rag_chain()

    return chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )


def answer_question(
    question: str,
    k: int = 3,
) -> dict:
    """
    Baseline RAG pipeline:

    retrieve → generate
    """
    documents = retrieve_documents(
        question,
        k=k,
    )

    answer = generate_answer(
        question,
        documents,
    )

    answered = NOT_FOUND_MESSAGE not in answer

    return {
        "answer": answer,
        "answered": answered,
        "documents": documents if answered else [],
    }