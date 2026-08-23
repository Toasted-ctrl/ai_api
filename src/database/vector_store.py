from dataclasses import dataclass
from sqlalchemy.orm import Session

from core.logging import get_logger
from database.schemas.vector_store import VectorStoreSettingsT
from database.schemas.vector_store_collections import VectorStoreCollectionT

log = get_logger()


@dataclass(frozen=True)
class VectorStoreConfig:
    vs_collection_name: str
    vs_encrypted_api_key: str
    vs_vendor: str
    vs_base_url: str
    vs_port: int
    e_dimensions: int
    e_provider: str
    e_model: str
    access_type: str
    required_filters: list


def get_vector_store_settings(
    collection_name: str,
    session: Session
) -> VectorStoreConfig:
    """Fetches and returns the Vector Store collection and configuration details, 
    to enable building a Vector Store client."""

    log.debug(f"Retrieving Vector Store settings for collection name '{collection_name}' ...")
    col: VectorStoreCollectionT = (
        session.query(VectorStoreCollectionT)
        .filter(VectorStoreCollectionT.name == collection_name)
        .one_or_none()
    )

    if not col:
        log.info(f"No Vector Store found with collection name '{collection_name}'.")
        raise ValueError(f"Vector Store with name '{collection_name}' does not exist ...")

    vs: VectorStoreSettingsT = (
        session.query(VectorStoreSettingsT)
        .filter(VectorStoreSettingsT.id == col.vector_store_id)
        .one_or_none()
    )

    if not vs:
        log.error(f"No Vector Store instance found with id '{col.vector_store_id}'.")
        raise ValueError(f"Vector Store instance with id '{col.vector_store_id}' does not exist.")

    log.debug("Returning Vector Store client.")
    return VectorStoreConfig(
        vs_collection_name=col.name,
        e_dimensions=col.e_dimensions,
        e_provider=col.e_provider,
        e_model=col.e_model,
        vs_encrypted_api_key=vs.encrypted_api_key,
        access_type=col.access_type,
        vs_vendor=vs.vendor,
        vs_base_url=vs.base_url,
        vs_port=vs.port,
        required_filters=col.required_filters
    )