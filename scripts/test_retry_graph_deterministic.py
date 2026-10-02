from langchain_core.documents import Document
from langgraph.graph import StateGraph, END

from app.graph.state import GraphState
from app.graph.edges import route_after_grade


def fake_retrieve(state: GraphState) -> dict:
    """Always return a document so the graph can continue to grading."""
    print(f"  RETRIEVE: query = {state['search_query']}")

    document = Document(
        page_content="Fake document for retry-loop testing.",
        metadata={
            "source": "retry_test.pdf",
            "start_page": 1,
            "end_page": 1,
            "chunk_index": 0,
        },
    )

    return {
        "documents": [document],
    }


def fake_grade(state: GraphState) -> dict:
    """Always report insufficient evidence."""
    print("  GRADE: insufficient")

    return {
        "relevant_documents": [],
        "sufficient": False,
        "grade_reason": "Fake grader: insufficient evidence.",
    }


def fake_rewrite(state: GraphState) -> dict:
    """Increment rewrite count and change the search query."""
    new_count = state["rewrite_count"] + 1
    new_query = f"rewritten query {new_count}"

    print(f"  REWRITE #{new_count}: {new_query}")

    return {
        "search_query": new_query,
        "rewrite_count": new_count,
    }


def build_test_graph():
    graph = StateGraph(GraphState)

    graph.add_node("retrieve", fake_retrieve)
    graph.add_node("grade", fake_grade)
    graph.add_node("rewrite", fake_rewrite)

    graph.set_entry_point("retrieve")

    graph.add_edge("retrieve", "grade")

    graph.add_conditional_edges(
        "grade",
        route_after_grade,
        {
            "generate": END,
            "rewrite": "rewrite",
            "fallback": END,
        },
    )

    graph.add_edge("rewrite", "retrieve")

    return graph.compile()


def main():
    print("=" * 70)
    print("DETERMINISTIC RETRY GRAPH TEST")
    print("=" * 70)
    print()

    graph = build_test_graph()

    initial_question = "How does TCP work when congestion happens?"

    initial_state = {
        "question": initial_question,
        "search_query": initial_question,
        "documents": [],
        "relevant_documents": [],
        "sufficient": False,
        "grade_reason": "",
        "rewrite_count": 0,
        "answer": "",
        "answered": False,
    }

    print("Running deterministic failure path...")
    print()

    result = graph.invoke(initial_state)

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"Original question:")
    print(f"  {result['question']}")

    print()
    print(f"Final search query:")
    print(f"  {result['search_query']}")

    print()
    print(f"Rewrite count:")
    print(f"  {result['rewrite_count']}")

    print()
    print(f"Sufficient:")
    print(f"  {result['sufficient']}")

    print()

    assert result["question"] == initial_question
    assert result["rewrite_count"] == 2
    assert result["search_query"] == "rewritten query 2"
    assert result["sufficient"] is False

    print("Original question preserved: PASS")
    print("Exactly 2 rewrites performed: PASS")
    print("Search query rewritten: PASS")
    print("Insufficient evidence preserved: PASS")
    print("Graph terminated after bounded retries: PASS")

    print()
    print("Deterministic retry graph test passed.")


if __name__ == "__main__":
    main()