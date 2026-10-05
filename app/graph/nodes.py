from app.graph.state import GraphState
from app.rag.chain import generate_answer, retrieve_documents
from app.rag.prompt import NOT_FOUND_MESSAGE


def retrieve_node(state: GraphState) -> dict:
    documents = retrieve_documents(
        state["search_query"],
        k=3,
    )

    return {
        "documents": documents,
    }


def generate_node(state: GraphState) -> dict:
    """
    Generate the final answer using the relevant documents
    selected by the retrieval grader.
    """
    answer = generate_answer(
        state["question"],
        state["relevant_documents"],
    )

    return {
        "answer": answer,
        "answered": NOT_FOUND_MESSAGE not in answer,
    }


def fallback_node(state: GraphState) -> dict:
    return {
        "answer": NOT_FOUND_MESSAGE,
        "answered": False,
    }