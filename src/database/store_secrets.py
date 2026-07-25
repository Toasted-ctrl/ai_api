from dataclasses import dataclass
from sqlalchemy.orm import Session
import uuid

from auth.create_secret import create_secret
from auth.hash import get_hash_sha356
from core.logging import get_logger
from database.schemas import ApiKeys

log = get_logger()


@dataclass(frozen=True)
class StoredClient:
    """Represents the generated secrets and metadata returned after storing a new API key."""
    client_api_key: str
    client_hmac_secret: str
    client_id: uuid.UUID
    client_key_type: str


def store_secrets(
    session: Session,
    client: str,
    key_type: str,
    owner_email: str,
    require_jwt: bool = True,
    require_external_id: bool = True,
    is_active: bool = True,
    api_key: str | None = None,
    hmac_secret: str | None = None
) -> StoredClient:

    """Generates and stores a new API key for a client / user.
    Action still needs to be committed."""

    log.debug("Generating new secrets...")

    if key_type not in ['User', 'Application']:
        raise ValueError("Key_type must be 'User' or 'Application'")

    # TODO: Build a better email check
    if not owner_email or owner_email == "":
        raise ValueError("A valid owner email must be provided")

    if api_key is None:
        cl_key = create_secret()
        db_key = get_hash_sha356(cl_key)

    else:
        cl_key = api_key
        db_key = get_hash_sha356(api_key)

    if hmac_secret is None:
        hmac = create_secret()

    else:
        hmac = hmac_secret

    if session.query(ApiKeys).filter(ApiKeys.client == client, ApiKeys.owner_email == owner_email).count() == 1:
        raise ValueError(f"Client '{client}' with owner '{owner_email}' already exists, skipping...")

    key = ApiKeys(
        api_key_hash=db_key,
        client=client,
        require_jwt=require_jwt,
        key_type=key_type,
        owner_email=owner_email,
        require_external_id=require_external_id,
        is_active=is_active,
        hmac_secret_hash=hmac
    )

    session.add(key)
    session.flush()

    log.debug("Secrets generated...")

    return StoredClient(
        client_api_key=cl_key,
        client_hmac_secret=hmac,
        client_id=key.id,
        client_key_type=key_type
    )