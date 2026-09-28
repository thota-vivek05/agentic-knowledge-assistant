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
    Replace existing chunks for the given sources with the
    current chunks.

    The same source document and chunk index always receive
    the same stable document ID.

    Deleting the existing source chunks first prevents stale
    chunks from remaining when a document becomes smaller
    after re-ingestion.
    """

    documents = []
    ids = []

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

    # Remove previous chunks for these sources.
    # This prevents stale chunks when a document shrinks.
    sources = {
        chunk["metadata"]["source"]
        for chunk in chunks
    }

    for source in sources:
        vectorstore.delete(
            where={"source": source}
        )

    # Add the current version of the chunks.
    vectorstore.add_documents(
        documents=documents,
        ids=ids,
    )

    return ids