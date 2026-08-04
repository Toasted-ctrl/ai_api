from dataclasses import dataclass
from sqlalchemy.orm import Session
import uuid

from core.logging import get_logger
from database.store_client import store_client
from database.person import get_or_store_person
from database.store_user import store_user

log = get_logger()

# TODO: Build tests.

@dataclass(frozen=True)
class StoredBackendUser:
    api_key: str
    hmac_secret: str
    owner_email: str
    key_type: str
    user_id: uuid.UUID


def create_backend_client_user(
    session: Session,
    client_name: str,
    key_type: str,
    owner_email: str,
    first_name: str,
    last_name: str,
    require_jwt: bool = False,
    require_external_id: bool = False,
    api_key: str | None = None,
    hmac_secret: str | None = None
) -> StoredBackendUser:

    """Creates a new Backend Client User. Returns None if the Backend Client User already exists, or runs into an error.
    If an error occurs, a rollback will be issued."""

    log.info("Starting Creation of new Backend Client User...")

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

    _person = get_or_store_person(
        session=session,
        first_name=first_name,
        last_name=last_name,
        email=owner_email
    )

    _user = store_user(
        session=session,
        person_id=_person.id,
        api_key_id=_client.id,
        key_type=_client.key_type
    )

    log.info(f"Created new Backend Client User: '{_user.id}'...")

    return StoredBackendUser(
        api_key=_client.api_key,
        hmac_secret=_client.hmac_secret,
        owner_email=_client.owner_email,
        key_type=_client.key_type,
        user_id=_user.id
    )