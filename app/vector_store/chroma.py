from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.embeddings.embedder import create_embedding_model


CHROMA_DIR = Path("vectorstore/chroma")
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
    Add new chunks and update existing chunks using stable IDs.

    The same source document and chunk index always receive
    the same document ID.
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

    # Check which IDs already exist
    existing_documents = vectorstore.get_by_ids(ids)

    existing_ids = {
        document.id
        for document in existing_documents
        if document.id
    }

    new_documents = []
    new_ids = []

    updated_documents = []
    updated_ids = []

    for document, document_id in zip(documents, ids):

        if document_id in existing_ids:

            updated_documents.append(document)
            updated_ids.append(document_id)

        else:

            new_documents.append(document)
            new_ids.append(document_id)

    # Add new documents
    if new_documents:

        vectorstore.add_documents(
            documents=new_documents,
            ids=new_ids,
        )

    # Update existing documents
    if updated_documents:

        vectorstore.update_documents(
            ids=updated_ids,
            documents=updated_documents,
        )

    return ids