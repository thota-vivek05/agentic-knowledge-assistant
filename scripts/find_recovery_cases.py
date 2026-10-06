from app.graph.grader import grade_documents
from app.graph.rewrite import rewrite_query
from app.graph.nodes import retrieve_node
from app.graph.state import GraphState


# These are deliberately phrased differently from the terminology
# used in the source document. The goal is to find cases where the
# initial retrieval may be insufficient but a rewritten query can
# recover the relevant evidence.
CANDIDATE_QUESTIONS = [
    "How does TCP increase its transmission capacity when starting a connection?",
    "How does TCP react after detecting that the network is overloaded?",
    "How does TCP gradually increase the amount of data it can send?",
    "How does TCP reduce its sending rate when packets are lost?",
    "How does TCP recover from congestion without continuously overwhelming the network?",
    "How does TCP change its behavior after congestion is detected?",
    "How does TCP control the amount of traffic it puts into the network?",
    "How does TCP increase and decrease its congestion window?",
    "What mechanisms does TCP use to control network traffic?",
    "How does TCP adjust its transmission behavior based on network conditions?",
]


def make_initial_state(question: str) -> GraphState:
    return {
        "question": question,
        "search_query": question,
        "documents": [],
        "relevant_documents": [],
        "sufficient": False,
        "grade_reason": "",
        "rewrite_count": 0,
        "answer": "",
        "answered": False,
    }


def describe_documents(documents) -> None:
    if not documents:
        print("  No documents retrieved.")
        return

    for document in documents:
        metadata = document.metadata

        source = metadata.get("source", "unknown")
        chunk_index = metadata.get("chunk_index", "unknown")
        start_page = metadata.get("start_page", "?")
        end_page = metadata.get("end_page", "?")

        preview = document.page_content.replace("\n", " ")
        preview = preview[:180]

        print(
            f"  chunk={chunk_index} "
            f"pages={start_page}-{end_page} "
            f"source={source}"
        )
        print(f"    {preview}...")


def run_candidate(question: str) -> bool:
    print("=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    # ---------------------------------------------------------
    # 1. Initial retrieval
    # ---------------------------------------------------------
    state = make_initial_state(question)

    retrieval_result = retrieve_node(state)
    state.update(retrieval_result)

    print("\nINITIAL SEARCH QUERY")
    print(state["search_query"])

    print("\nINITIAL RETRIEVAL")
    describe_documents(state["documents"])

    # ---------------------------------------------------------
    # 2. Initial grading
    # ---------------------------------------------------------
    grade_result = grade_documents(state)
    state.update(grade_result)

    print("\nINITIAL GRADE")
    print(f"  Sufficient: {state['sufficient']}")
    print(f"  Reason: {state['grade_reason']}")

    if state["sufficient"]:
        print("\nRESULT")
        print("  Initial retrieval was already sufficient.")
        print("  This is NOT a recovery case.")

        return False

    # ---------------------------------------------------------
    # 3. Rewrite query
    # ---------------------------------------------------------
    rewrite_result = rewrite_query(state)
    state.update(rewrite_result)

    print("\nREWRITTEN QUERY")
    print(state["search_query"])
    print(f"Rewrite count: {state['rewrite_count']}")

    # ---------------------------------------------------------
    # 4. Retrieval using rewritten query
    # ---------------------------------------------------------
    retrieval_result = retrieve_node(state)
    state.update(retrieval_result)

    print("\nRETRIEVAL AFTER REWRITE")
    describe_documents(state["documents"])

    # ---------------------------------------------------------
    # 5. Grade rewritten retrieval
    # ---------------------------------------------------------
    grade_result = grade_documents(state)
    state.update(grade_result)

    print("\nGRADE AFTER REWRITE")
    print(f"  Sufficient: {state['sufficient']}")
    print(f"  Reason: {state['grade_reason']}")

    # ---------------------------------------------------------
    # 6. Determine whether genuine recovery occurred
    # ---------------------------------------------------------
    if state["sufficient"]:
        print("\n" + "=" * 80)
        print("✓ GENUINE RECOVERY CASE FOUND")
        print("=" * 80)

        print(f"Question: {question}")
        print("Initial retrieval: insufficient")
        print("Query rewrite: successful")
        print("Rewritten retrieval: sufficient")

        return True

    print("\nRESULT")
    print("  Rewrite did not recover sufficient evidence.")

    return False


def main() -> None:
    print("=" * 80)
    print("RECOVERY CASE SEARCH")
    print("=" * 80)

    recovery_cases = []

    for index, question in enumerate(CANDIDATE_QUESTIONS, start=1):
        print(f"\n\n[{index}/{len(CANDIDATE_QUESTIONS)}]")

        try:
            recovered = run_candidate(question)

            if recovered:
                recovery_cases.append(question)

        except Exception as exc:
            print("\nERROR")
            print(f"  {type(exc).__name__}: {exc}")

    # ---------------------------------------------------------
    # Final summary
    # ---------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("RECOVERY SEARCH SUMMARY")
    print("=" * 80)

    print(f"Candidates tested: {len(CANDIDATE_QUESTIONS)}")
    print(f"Genuine recovery cases: {len(recovery_cases)}")

    if recovery_cases:
        print("\nRecovery cases found:")

        for index, question in enumerate(recovery_cases, start=1):
            print(f"  {index}. {question}")

        print("\n✓ These cases can be candidates for the recovery benchmark.")

    else:
        print("\nNo genuine recovery cases were found.")
        print(
            "Do not modify the system just to force a recovery case."
        )


if __name__ == "__main__":
    main()