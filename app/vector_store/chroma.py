from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.embeddings.embedder import create_embedding_model


CHROMA_DIR = (
    Path(__file__).resolve().parents[2]
    / "vectorstore"
    / "chroma"
)

COLLECTION_NAME = "knowledge_base"


def create_vectorstore() -> Chroma:
    """
    Create or load the persistent ChromaDB vector store.
    """

    embedding_model = create_embedding_model()

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_DIR),
    )

    return vectorstore


def add_chunks(
    vectorstore: Chroma,
    chunks: list[dict],
) -> list[str]:
    """
    Upsert the current chunks, then remove stale chunks.

    Upserting first means a failure during embedding or indexing
    does not delete the previously indexed version of the document.

    Stale chunks are deleted only after the current chunks have
    been successfully added.

    If chunks is empty, nothing is changed and an empty list is returned.
    """

    # Empty input is a no-op.
    if not chunks:
        return []

    documents = []
    ids = []

    # ---------------------------------------------------------
    # Build LangChain Documents and stable IDs
    # ---------------------------------------------------------

    for chunk in chunks:

        metadata = chunk["metadata"]

        source = metadata["source"]
        chunk_index = metadata["chunk_index"]

        document_id = f"{source}::chunk_{chunk_index}"

        document = Document(
            page_content=chunk["text"],
            metadata=metadata,
        )

        documents.append(document)
        ids.append(document_id)

    # ---------------------------------------------------------
    # 1. Upsert the current chunks first
    #
    # Existing IDs are overwritten.
    # New IDs are added.
    #
    # This happens BEFORE stale chunks are removed.
    # ---------------------------------------------------------

    vectorstore.add_documents(
        documents=documents,
        ids=ids,
    )

    # ---------------------------------------------------------
    # 2. Remove stale chunks
    #
    # Example:
    #
    # Previous:
    #   chunk_0
    #   chunk_1
    #   chunk_2
    #   chunk_3
    #   chunk_4
    #
    # New:
    #   chunk_0
    #   chunk_1
    #   chunk_2
    #
    # chunk_3 and chunk_4 are stale and get deleted.
    # ---------------------------------------------------------

    current_ids = set(ids)

    sources = {
        chunk["metadata"]["source"]
        for chunk in chunks
    }

    for source in sources:

        stored_data = vectorstore.get(
            where={"source": source},
            include=[],
        )

        stored_ids = stored_data["ids"]

        stale_ids = [
            document_id
            for document_id in stored_ids
            if document_id not in current_ids
        ]

        if stale_ids:
            vectorstore.delete(
                ids=stale_ids
            )

    return ids