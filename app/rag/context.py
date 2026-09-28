def format_location(metadata: dict) -> str:
    """
    Format page information from document metadata.
    """

    start_page = metadata.get("start_page")
    end_page = metadata.get("end_page")

    if start_page is None:
        return "page unknown"

    if end_page is None or start_page == end_page:
        return f"page {start_page}"

    return f"pages {start_page}-{end_page}"


def format_context(documents) -> str:
    """
    Convert retrieved LangChain Documents into a context string
    containing text and source metadata.
    """

    context_parts = []

    for index, document in enumerate(
        documents,
        start=1,
    ):

        metadata = document.metadata

        source = metadata.get(
            "source",
            "Unknown source",
        )

        location = format_location(
            metadata
        )

        chunk_index = metadata.get(
            "chunk_index",
            "unknown",
        )

        context_parts.append(
            f"""
[Context {index}]
Source: {source}
Location: {location}
Chunk: {chunk_index}

{document.page_content}
""".strip()
        )

    return "\n\n".join(context_parts)


def format_sources(documents) -> list[str]:
    """
    Format retrieved documents as user-visible source citations.

    Sources are generated from metadata rather than by the LLM.
    """

    sources = []

    for document in documents:

        metadata = document.metadata

        source = metadata.get(
            "source",
            "Unknown source",
        )

        location = format_location(
            metadata
        )

        chunk_index = metadata.get(
            "chunk_index",
            "unknown",
        )

        sources.append(
            f"{source}, "
            f"{location} "
            f"(chunk {chunk_index})"
        )

    return sources