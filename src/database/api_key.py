from sqlalchemy.orm import Session
import secrets

from database.schemas import ApiKeys

def create_api_key(
    db: Session,
    client: str,
    require_jwt: bool = True,
    require_external_id: bool = True,
    is_active: bool = True
):

    api_key = secrets.token_hex(32)
    hmac_secret = secrets.token_hex(32)

    if db.query(ApiKeys).filter(ApiKeys.client == client).count() == 1:
        raise ValueError(f"Client '{client}' already exists")

    key = ApiKeys(
        api_key=api_key,
        client=client,
        require_jwt=require_jwt,
        require_external_id=require_external_id,
        is_active=is_active,
        hmac_secret=hmac_secret
    )

    db.add(key)
    return api_key