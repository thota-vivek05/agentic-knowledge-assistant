from app.rag.chain import retrieve_documents
from app.rag.prompt import NOT_FOUND_MESSAGE
from app.graph.state import GraphState


def retrieve_node(state: GraphState) -> dict:
    documents = retrieve_documents(
        state["search_query"],
        k=3,
    )

    return {
        "documents": documents,
    }


def fallback_node(state: GraphState) -> dict:
    return {
        "answer": NOT_FOUND_MESSAGE,
        "answered": False,
    }