from dataclasses import dataclass
from sqlalchemy.orm import Session
import uuid

from core.logging import get_logger
from database.schemas import Users

log = get_logger()

@dataclass(frozen=True)
class StoredUser:
    id: uuid.UUID


def store_user(
    session: Session,
    person_id: uuid.UUID,
    api_key_id: uuid.UUID,
    key_type: str,
    external_id: str | None = None,
) -> StoredUser:

    if key_type == 'Application' and external_id == None:
        raise ValueError("Unable to add User, if key_type = 'Application', external_id must not be None")

    if session.query(Users).filter(
        Users.api_key_id == api_key_id,
        Users.person_id == person_id
    ).count() == 1:
        raise ValueError("User already exists, skipping...")

    user = Users(
        person_id=person_id,
        api_key_id=api_key_id,
        external_id=external_id
    )

    session.add(user)
    session.flush()

    log.info(f"Added User with id: {user.id}")

    return StoredUser(
        id=user.id
    )


def get_or_store_user(
    session: Session,
    person_id: uuid.UUID,
    api_key_id: uuid.UUID,
    key_type: str,
    login_provider: str | None = None,
    external_id: str | None = None,
) -> StoredUser:

    if key_type == 'Application' and external_id == None:
        raise ValueError("Unable to add User, if key_type = 'Application', external_id must not be None")

    stored_user = (
        session.query(Users)
        .filter(
            Users.person_id == person_id,
            Users.api_key_id == api_key_id,
            Users.external_id == external_id,
            Users.login_provider == login_provider
        )
        .first()
    )
    if stored_user:
        log.info(f"User already exists, returning existing record: '{stored_user.id}'...")
        return StoredUser(
            id=stored_user.id
        )

    user = Users(
        person_id=person_id,
        api_key_id=api_key_id,
        external_id=external_id,
        login_provider=login_provider
    )

    session.add(user)
    session.flush()

    log.info(f"Added User with id: {user.id}")

    return StoredUser(
        id=user.id
    )