from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore

from core.logging import get_logger

log = get_logger()


def save_docs(
    vector_store: QdrantVectorStore,
    texts: list[str],
    metadatas: list[dict] | None = None,
    required_metadata: list[str] | None = None
) -> list[str]:
    """Adds documents to indicated Vector Store.
    Currently only Qdrant supported."""

    if metadatas and required_metadata:
        for metadata in metadatas:
            keys = metadata.keys()
            if not all(req in keys for req in required_metadata):
                raise ValueError("Missing required metadata ...")

    # TODO: This function can now create duplicates. Perhaps we should make a check for
    # if an item is a duplicate for the user.

    match vector_store:
        case QdrantVectorStore():
            log.debug("Saving documents to Qdrant vector store ...")
            pass

            # TODO: Add processing for Qdrant
            # TODO: Also ensure we cannot add duplicates

        case _:
            log.error(f"Unsupported Vector Store detected: {type(vector_store).__name__} ...")
            raise ValueError(f"Unsupported Vector Store type: {type(vector_store).__name__}")