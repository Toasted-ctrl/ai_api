from dataclasses import dataclass
from fastapi import Security, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.orm import Session
import uuid

from core.logging import get_logger
from database.schemas.clients import ClientsT
from database.session import get_db_session
from security.hash import get_hash_sha256

log = get_logger()

api_key_header = APIKeyHeader(name="X-API-Key")


@dataclass(frozen=True)
class VerifiedClient:
    id: uuid.UUID
    key_type: str


def depends_get_client(
    api_key: str = Security(api_key_header),
    session: Session = Depends(get_db_session)
) -> VerifiedClient:

    """Verifies that the client belonging to the API key exists in the database.
    Return VerifiedClient dataclass if so, else raises HTTPException."""

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key"
        )

    try:
        client = session.query(ClientsT).filter(ClientsT.api_key_hash == get_hash_sha256(api_key)).one_or_none()
    except MultipleResultsFound:
        log.critical(f"Multiple Clients matched with single API key hash: {get_hash_sha256(api_key)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error. Please contact your administrator."
        )

    if not client:
        log.warning(f"API key authentication failed - no matching client for API key hash: {get_hash_sha256(api_key)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )

    log.debug(f"Verified Client: {client.id}")
    return VerifiedClient(
        id=client.id,
        key_type=client.key_type
    )


def depends_get_application_client(
    client: VerifiedClient = Depends(depends_get_client)
) -> VerifiedClient:

    """Verifying if the client is a frontend application client.
    Returns VerifiedClient dataclass, otherwise raises HTTPException."""

    if client.key_type != "Application":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client must be a frontend application, with a login requirement."
        )

    return client