from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import Filter, FieldCondition, MatchValue
import uuid

from core.logging import get_logger

log = get_logger()


def qdrant_store_docs(
    vector_store: QdrantVectorStore,
    texts: list[str],
    user_id: uuid.UUID,
    metadatas: list[dict] | None = None
) -> list[str]:
    """Adds documents to the Qdrant vector store instance."""

    log.debug(f"Storing {len(texts)} documents into Qdrant ...")

    documents = [
        Document(
            page_content=text,
            metadata={"user_id": str(user_id), **(metadatas[i] if metadatas else {})}
        )
        for i, text in enumerate(texts)
    ]

    ids = vector_store.add_documents(documents)

    log.debug(f"Stored {len(ids)} documents successfully.")

    return ids


def qdrant_search_documents(
    query: str,
    vector_store: QdrantVectorStore,
    user_id: uuid.UUID,
    k: int = 5,
    score_threshold: float = 0.7
) -> list[Document]:
    """Returns a list of documents from the vector store."""

    log.debug("Searching in Qdrant collection ...")

    results = vector_store.similarity_search(
        query=query,
        k=k,
        filter=Filter(
            must=[
                FieldCondition(
                    key="metadata.user_id",
                    match=MatchValue(value=str(user_id))
                )
            ]
        )
    )

    filtered = [
        doc for doc, score in results if score >= score_threshold
    ]

    log.debug(f"Found {len(filtered)} results, returning ...")

    return filtered