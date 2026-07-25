from core.config import config
from core.logging import get_logger
from database.session import get_db_session
from database.store_secrets import store_secrets, StoredClient

log = get_logger()

def create_frontend_client(
    client: str,
    key_type: str,
    owner_email: str,
    require_jwt: bool,
    require_external_id: bool,
    api_key: str | None = None,
    hmac_secret: str | None = None
) -> StoredClient:

    log.debug("Creating new frontend client")
    with get_db_session(db_url=config.PG_DB_URL) as session:

        try:
            
            user = store_secrets(
                session=session,
                client=client,
                key_type=key_type,
                owner_email=owner_email,
                require_jwt=require_jwt,
                require_external_id=require_external_id,
                api_key=api_key,
                hmac_secret=hmac_secret
            )

            log.debug("Created new frontend client...")
            return user

        except ValueError as e:
            log.warning(e)
            return