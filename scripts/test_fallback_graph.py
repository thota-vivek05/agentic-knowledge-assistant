from langgraph.graph import StateGraph, END

from app.graph.state import GraphState
from app.graph.edges import route_after_grade
from app.graph.nodes import fallback_node


def fake_retrieve(state: GraphState) -> dict:
    return {
        "documents": [],
    }


def fake_grade(state: GraphState) -> dict:
    return {
        "relevant_documents": [],
        "sufficient": False,
        "grade_reason": "Fake grader: insufficient evidence.",
    }


def build_test_graph():
    graph = StateGraph(GraphState)

    graph.add_node("retrieve", fake_retrieve)
    graph.add_node("grade", fake_grade)
    graph.add_node("fallback", fallback_node)

    graph.set_entry_point("retrieve")

    graph.add_edge("retrieve", "grade")

    graph.add_conditional_edges(
        "grade",
        route_after_grade,
        {
            "generate": END,
            "rewrite": END,
            "fallback": "fallback",
        },
    )

    graph.add_edge("fallback", END)

    return graph.compile()


def main():
    print("=" * 70)
    print("FALLBACK GRAPH TEST")
    print("=" * 70)
    print()

    graph = build_test_graph()

    initial_state = {
        "question": "What is TCP CUBIC?",
        "search_query": "TCP CUBIC",
        "documents": [],
        "relevant_documents": [],
        "sufficient": False,
        "grade_reason": "",
        "rewrite_count": 2,
        "answer": "",
        "answered": False,
    }

    print("Running fallback path...")
    print()

    result = graph.invoke(initial_state)

    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    print("Answer:")
    print(result["answer"])

    print()
    print(f"Answered: {result['answered']}")
    print(f"Rewrite count: {result['rewrite_count']}")

    assert result["answer"] == (
        "I don't have enough information in the provided documents "
        "to answer that question."
    )

    assert result["answered"] is False
    assert result["rewrite_count"] == 2

    print()
    print("Fallback node reached: PASS")
    print("Correct fallback message: PASS")
    print("Answered flag is False: PASS")
    print("Retry count preserved: PASS")
    print()
    print("Fallback graph test passed.")


if __name__ == "__main__":
    main()