from dataclasses import dataclass
from sqlalchemy.orm import Session
import uuid

from database.person import get_or_store_person, StoredPerson
from database.store_user import get_or_store_user, StoredUser

@dataclass(frozen=True)
class VerifiedApplicationUser:
    client_id: uuid.UUID
    user_id: uuid.UUID
    person_id: uuid.UUID


def get_or_create_application_user(
    first_name: str,
    last_name: str,
    client_id: uuid.UUID,
    login_provider: str,
    email: str,
    external_id: str,
    session: Session
) -> VerifiedApplicationUser:

    person: StoredPerson = get_or_store_person(
        session=session,
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    user: StoredUser = get_or_store_user(
        session=session,
        person_id=person.id,
        api_key_id=client_id,
        key_type="Application",
        login_provider=login_provider,
        external_id=external_id
    )

    return VerifiedApplicationUser(
        client_id=client_id,
        user_id=user.id,
        person_id=person.id
    )