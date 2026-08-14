from dataclasses import dataclass
from sqlalchemy.orm import Session
import uuid

from core.logging import get_logger
from database.schemas.clients import ClientsT


log = get_logger()


@dataclass(frozen=True)
class ApplicationClient:
    id: uuid.UUID
    encrypted_redirect_uri: str


def get_client_from_client_id(
    session: Session,
    client_id: uuid.UUID
) -> ApplicationClient | None:
    """Returns an ApplicationClient object based on a provided client_id.
    Will return None if no Client is found."""

    client = (
        session.query(ClientsT)
        .filter(ClientsT.id == client_id)
        .one_or_none()
    )

    if not client:
        log.warning(f"Invalid Client ID: {client_id}")
        raise LookupError(f"Invalid Client ID: {client_id}")

    log.debug(f"Returning ApplicationClient object for Client ID: '{client_id}' ...")

    return ApplicationClient(
        id=client.id,
        encrypted_redirect_uri=client.encrypted_redirect_uri
    )