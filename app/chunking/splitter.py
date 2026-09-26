from collections import defaultdict

from langchain_text_splitters import RecursiveCharacterTextSplitter


CHUNK_SIZE = 2400
CHUNK_OVERLAP = 360


def create_splitter() -> RecursiveCharacterTextSplitter:
    """
    Create the recursive text splitter.

    Approximately targets:
    - 600 tokens per chunk
    - 15% overlap
    """

    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )


def chunk_pages(pages: list[dict]) -> list[dict]:
    """
    Combine pages belonging to the same document and split them
    into overlapping chunks while preserving page ranges.
    """

    splitter = create_splitter()

    # Group pages by source document
    documents = defaultdict(list)

    for page in pages:
        source = page["metadata"]["source"]
        documents[source].append(page)

    chunks = []

    for source, document_pages in documents.items():

        # Ensure correct page order
        document_pages.sort(
            key=lambda page: page["metadata"]["page"]
        )

        # Build document text and track where each page begins/ends
        document_text = ""
        page_boundaries = []

        for page in document_pages:

            page_number = page["metadata"]["page"]
            text = page["text"].strip()

            if not text:
                continue

            # Add separator between pages
            if document_text:
                document_text += "\n\n"

            start_position = len(document_text)

            document_text += text

            end_position = len(document_text)

            page_boundaries.append(
                {
                    "page": page_number,
                    "start": start_position,
                    "end": end_position,
                }
            )

        if not document_text:
            continue

        # Ask the splitter for chunks while retaining character positions
        split_documents = splitter.create_documents(
            [document_text]
        )

        for chunk_index, document in enumerate(split_documents):

            chunk_text = document.page_content

            # Find the position of this chunk inside the original document
            chunk_start = document_text.find(chunk_text)

            if chunk_start == -1:
                start_page = None
                end_page = None
            else:
                chunk_end = chunk_start + len(chunk_text)

                overlapping_pages = [
                    boundary["page"]
                    for boundary in page_boundaries
                    if (
                        chunk_start < boundary["end"]
                        and chunk_end > boundary["start"]
                    )
                ]

                if overlapping_pages:
                    start_page = min(overlapping_pages)
                    end_page = max(overlapping_pages)
                else:
                    start_page = None
                    end_page = None

            first_page_metadata = document_pages[0]["metadata"]

            metadata = {
                "source": source,
                "start_page": start_page,
                "end_page": end_page,
                "chunk_index": chunk_index,
                "type": first_page_metadata["type"],
            }

            chunks.append(
                {
                    "text": chunk_text,
                    "metadata": metadata,
                }
            )

    return chunks