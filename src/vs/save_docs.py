from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
import hashlib

from core.logging import get_logger
from vs.count import count_tokens

log = get_logger()


def _chunker(
    text: str,
    max_tokens: int = 500,
    overlap: int = 50
) -> list[str]:
    """Divides a provided body of text into chunks. Will return the full body as
    single chunk if the chunk is smaller than 500 tokens."""

    if count_tokens(text=text) <= 500:
        log.debug(f"Token count is less than or equal to 500, returning whole body ...")
        return [text]

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=max_tokens,
        chunk_overlap=overlap
    )

    log.debug("Initialized chunker.")
    split = splitter.split_text(text=text)
    log.debug(f"Created {len(split)} from body of text, returning ...")
    return split


def _prep_docs_personal_data(
    texts: list[str],
    metadatas: list[dict],
) -> list[Document]:
    """Prepares the data for ingestion. Will create 'Documents' for each piece of text to be ingested.
    Document preparation only intended for preparing PERSONAL data."""

    # TODO: Requires tests.

    documents = []
    for text, metadata in zip(texts, metadatas):
        document_hash = hashlib.sha256(text.encode()).hexdigest()
        user_id = str(metadata.get("user_id")) # NOTE: Likely to be a UUID.
        chunks = _chunker(text=text)
        for j, chunk in enumerate(chunks):
            document_id = f"{user_id}:{document_hash}:{j}"
            documents.append(
                Document(
                    id=document_id,
                    page_content=chunk,
                    metadata=metadata
                )
            )
    return documents


def save_docs(
    vector_store: QdrantVectorStore,
    texts: list[str],
    metadatas: list[dict] | None = None,
    required_metadata: list[str] | None = None
) -> list[str]:
    """Adds documents to indicated Vector Store.
    Currently only Qdrant supported."""

    if required_metadata and not metadatas:
        raise ValueError("required_metadata specified but no metadatas provided ...")

    if metadatas:
        if len(metadatas) != len(texts):
            raise ValueError(f"Length mismatch: {len(texts)} texts vs {len(metadatas)} metadatas ...")
        if required_metadata:
            for i, metadata in enumerate(metadatas):
                missing = [r for r in required_metadata if r not in metadata]
                if missing:
                    raise ValueError(f"Metadata at index {i} missing required keys: {missing} ...")

    # TODO: This function can now create duplicates. Perhaps we should make a check for
    # if an item is a duplicate for the user.

    # TODO: Maybe we also want to create a hash for each document uploaded?

    match vector_store:
        case QdrantVectorStore():
            log.debug("Saving documents to Qdrant vector store ...")
            pass

            # TODO: Add processing for Qdrant
            # TODO: Also ensure we cannot add duplicates

        case _:
            log.error(f"Unsupported Vector Store detected: {type(vector_store).__name__} ...")
            raise ValueError(f"Unsupported Vector Store type: {type(vector_store).__name__}")