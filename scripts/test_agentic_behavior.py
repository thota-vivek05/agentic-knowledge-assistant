from langgraph.graph import END, StateGraph

from app.graph.edges import MAX_REWRITES, route_after_grade
from app.graph.state import GraphState


def make_state() -> GraphState:
    return {
        "question": "How does TCP slow start work?",
        "search_query": "How does TCP slow start work?",
        "documents": [],
        "relevant_documents": [],
        "sufficient": False,
        "grade_reason": "",
        "rewrite_count": 0,
        "answer": "",
        "answered": False,
    }


def build_test_graph(
    grading_results: list[bool],
):
    """
    Build a deterministic graph that simulates the agentic
    retrieval/grading/rewrite loop.

    grading_results controls what the fake grader returns
    on each grading attempt.

    Example:
        [True]
        -> immediate success

        [False, True]
        -> one rewrite, then recovery

        [False, False, False]
        -> two rewrites, then fallback
    """

    state = {
        "grade_calls": 0,
        "retrieve_calls": 0,
        "rewrite_calls": 0,
    }

    def retrieve(state_value: GraphState) -> dict:
        state["retrieve_calls"] += 1

        return {
            "documents": [
                {
                    "text": f"fake document {state['retrieve_calls']}",
                    "metadata": {
                        "source": "test_document.pdf",
                        "chunk_index": state["retrieve_calls"],
                    },
                }
            ]
        }

    def grade(state_value: GraphState) -> dict:
        call_number = state["grade_calls"]
        state["grade_calls"] += 1

        if call_number >= len(grading_results):
            raise AssertionError(
                "The deterministic grader was called more times "
                "than expected."
            )

        sufficient = grading_results[call_number]

        return {
            "sufficient": sufficient,
            "relevant_documents": (
                state_value["documents"] if sufficient else []
            ),
            "grade_reason": (
                "Deterministic test: sufficient evidence."
                if sufficient
                else "Deterministic test: insufficient evidence."
            ),
        }

    def rewrite(state_value: GraphState) -> dict:
        state["rewrite_calls"] += 1

        return {
            "search_query": (
                f"rewritten query {state['rewrite_calls']}"
            ),
            "rewrite_count": state_value["rewrite_count"] + 1,
        }

    def generate(state_value: GraphState) -> dict:
        return {
            "answer": "Deterministic generated answer.",
            "answered": True,
        }

    def fallback(state_value: GraphState) -> dict:
        return {
            "answer": (
                "I don't have enough information in the provided "
                "documents to answer that question."
            ),
            "answered": False,
        }

    graph = StateGraph(GraphState)

    graph.add_node("retrieve", retrieve)
    graph.add_node("grade", grade)
    graph.add_node("rewrite", rewrite)
    graph.add_node("generate", generate)
    graph.add_node("fallback", fallback)

    graph.set_entry_point("retrieve")

    graph.add_edge("retrieve", "grade")

    graph.add_conditional_edges(
        "grade",
        route_after_grade,
        {
            "generate": "generate",
            "rewrite": "rewrite",
            "fallback": "fallback",
        },
    )

    graph.add_edge("rewrite", "retrieve")
    graph.add_edge("generate", END)
    graph.add_edge("fallback", END)

    return graph.compile(), state


def test_immediate_success() -> None:
    """
    Case A:

        retrieve
            ↓
        grade = sufficient
            ↓
        generate
    """

    graph, counters = build_test_graph([True])

    result = graph.invoke(make_state())

    assert result["sufficient"] is True
    assert result["answered"] is True
    assert result["rewrite_count"] == 0

    assert counters["retrieve_calls"] == 1
    assert counters["grade_calls"] == 1
    assert counters["rewrite_calls"] == 0

    print("✓ Case A: immediate success")


def test_successful_recovery() -> None:
    """
    Case B:

        retrieve
            ↓
        grade = insufficient
            ↓
        rewrite
            ↓
        retrieve
            ↓
        grade = sufficient
            ↓
        generate
    """

    graph, counters = build_test_graph([False, True])

    result = graph.invoke(make_state())

    assert result["sufficient"] is True
    assert result["answered"] is True
    assert result["rewrite_count"] == 1

    assert counters["retrieve_calls"] == 2
    assert counters["grade_calls"] == 2
    assert counters["rewrite_calls"] == 1

    assert result["search_query"] == "rewritten query 1"

    print("✓ Case B: successful recovery after one rewrite")


def test_retry_exhaustion() -> None:
    """
    Case C:

        retrieve
            ↓
        grade = insufficient
            ↓
        rewrite
            ↓
        retrieve
            ↓
        grade = insufficient
            ↓
        rewrite
            ↓
        retrieve
            ↓
        grade = insufficient
            ↓
        fallback
    """

    graph, counters = build_test_graph(
        [False, False, False]
    )

    result = graph.invoke(make_state())

    assert result["sufficient"] is False
    assert result["answered"] is False
    assert result["rewrite_count"] == MAX_REWRITES

    assert counters["retrieve_calls"] == MAX_REWRITES + 1
    assert counters["grade_calls"] == MAX_REWRITES + 1
    assert counters["rewrite_calls"] == MAX_REWRITES

    assert (
        result["answer"]
        == "I don't have enough information in the provided "
        "documents to answer that question."
    )

    print("✓ Case C: retry exhaustion reaches fallback")


def main() -> None:
    print("=" * 70)
    print("AGENTIC RAG BEHAVIOR TEST")
    print("=" * 70)

    print("\nTesting deterministic graph behavior...\n")

    test_immediate_success()
    test_successful_recovery()
    test_retry_exhaustion()

    print("\n" + "=" * 70)
    print("ALL AGENTIC BEHAVIOR TESTS PASSED")
    print("=" * 70)

    print("\nValidated behaviors:")
    print("  1. Immediate successful retrieval")
    print("  2. Recovery after insufficient retrieval")
    print("  3. Bounded retry loop")
    print("  4. Deterministic fallback")
    print(f"  5. Maximum rewrites: {MAX_REWRITES}")


if __name__ == "__main__":
    main()