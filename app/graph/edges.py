from app.graph.state import GraphState


MAX_REWRITES = 2


def route_after_grade(state: GraphState) -> str:
    """
    Decide what node should execute after document grading.

    Returns:
        "generate"  -> evidence is sufficient
        "rewrite"   -> evidence is insufficient but retries remain
        "fallback"  -> evidence is insufficient and retries are exhausted
    """

    if state["sufficient"]:
        return "generate"

    if state["rewrite_count"] < MAX_REWRITES:
        return "rewrite"

    return "fallback"