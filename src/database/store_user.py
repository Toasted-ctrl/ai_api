from sqlalchemy.orm import Session
import uuid

from core.logging import get_logger
from database.schemas import Users

log = get_logger()

# TODO: Create tests

def store_user(
    session: Session,
    person_id: uuid.UUID,
    api_key_id: uuid.UUID,
    key_type: str,
    external_id: str | None = None,
    
) -> None:

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

    return user.id