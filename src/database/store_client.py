from dataclasses import dataclass
from sqlalchemy.orm import Session
import uuid

from auth.create_secret import create_secret
from auth.hash import get_hash_sha256
from core.logging import get_logger
from database.schemas import ApiKeys

log = get_logger()


@dataclass(frozen=True)
class StoredClient:

    """Represents the generated secrets and metadata returned after storing a new API key."""

    api_key: str
    hmac_secret: str
    id: uuid.UUID
    key_type: str
    owner_email: str


def store_client(
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

    log.debug("Generating new client secrets...")

    if key_type not in ['User', 'Application']:
        raise ValueError("Key_type must be 'User' or 'Application'...")

    # TODO: Build a better email check
    if not owner_email or owner_email == "":
        raise ValueError("A valid owner email must be provided...")

    if session.query(ApiKeys).filter(ApiKeys.client == client, ApiKeys.owner_email == owner_email).count() == 1:
        raise ValueError(f"Client '{client}' with owner '{owner_email}' already exists, skipping...")

    if api_key is None:
        ext_key = create_secret()
        hsh_key = get_hash_sha256(ext_key)

    else:
        ext_key = api_key
        hsh_key = get_hash_sha256(api_key)

    if hmac_secret is None:
        hmac = create_secret()

    else:
        hmac = hmac_secret

    key = ApiKeys(
        api_key_hash=hsh_key,
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

    log.debug("Client stored and secrets generated...")

    return StoredClient(
        api_key=ext_key,
        hmac_secret=key.hmac_secret_hash,
        id=key.id,
        key_type=key.key_type,
        owner_email=key.owner_email
    )