from sqlalchemy.orm import Session

from core.logging import get_logger
from database.store_client import store_client, StoredClient

log = get_logger()

# TODO: Build tests.

def create_frontend_client(
    session: Session,
    client_name: str,
    key_type: str,
    owner_email: str,
    require_jwt: bool,
    require_external_id: bool,
    api_key: str | None = None,
    hmac_secret: str | None = None
) -> StoredClient:

    """Creates a new Frontend Application client."""

    log.debug("Creating new frontend client")
            
    _client = store_client(
        session=session,
        client_name=client_name,
        key_type=key_type,
        owner_email=owner_email,
        require_jwt=require_jwt,
        require_external_id=require_external_id,
        api_key=api_key,
        hmac_secret=hmac_secret
    )

    log.debug("Created new frontend client...")
    return _client