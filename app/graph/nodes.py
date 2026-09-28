from app.rag.chain import retrieve_documents
from app.graph.state import GraphState


def retrieve_node(state: GraphState) -> dict:
    """
    Retrieve documents using the current search query.

    The original question is preserved.
    Only the retrieved documents are added to the state.
    """

    documents = retrieve_documents(
        state["search_query"],
        k=3,
    )

    return {
        "documents": documents,
    }