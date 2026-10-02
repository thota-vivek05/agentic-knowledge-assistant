from langgraph.graph import StateGraph, END

from app.graph.state import GraphState
from app.graph.nodes import retrieve_node, fallback_node
from app.graph.grader import grade_documents
from app.graph.rewrite import rewrite_query
from app.graph.edges import route_after_grade


def build_retry_graph():
    graph = StateGraph(GraphState)

    # Nodes
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("grade", grade_documents)
    graph.add_node("rewrite", rewrite_query)
    graph.add_node("fallback", fallback_node)

    # Initial retrieval
    graph.set_entry_point("retrieve")

    # retrieve -> grade
    graph.add_edge("retrieve", "grade")

    # grade -> generate / rewrite / fallback
    graph.add_conditional_edges(
        "grade",
        route_after_grade,
        {
            "generate": END,
            "rewrite": "rewrite",
            "fallback": "fallback",
        },
    )

    # rewrite -> retrieve
    graph.add_edge("rewrite", "retrieve")

    # fallback -> END
    graph.add_edge("fallback", END)

    return graph.compile()