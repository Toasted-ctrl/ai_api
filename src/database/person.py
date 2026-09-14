import uuid
from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.config import config
from core.logging import get_logger
from database.schemas.persons_users import PersonsT
from security.encryption import encrypt, decrypt
from security.hmac import hash_hmac


log = get_logger()


@dataclass(frozen=True)
class PersonDetails:
    person_id: uuid.UUID
    first_name: str
    last_name: str
    email: str


def get_person_by_person_id(
    session: Session,
    person_id: uuid.UUID
) -> PersonDetails | None:
    """Retrieves a Person's data by searching for their ID."""

    person = (
        session.query(PersonsT)
        .filter(PersonsT.id == person_id)
        .one_or_none()
    )

    if not person:
        return None

    return PersonDetails(
        person_id=person.id,
        first_name=decrypt(person.encrypted_first_name),
        last_name=decrypt(person.encrypted_last_name),
        email=decrypt(person.encrypted_email)
    )


@dataclass(frozen=True)
class Person:
    id: uuid.UUID


def get_or_store_person(
    session: Session,
    first_name: str,
    last_name: str,
    email: str
) -> Person:

    """Stores a new or retrieves an existing person from the database."""

    blind_index_email_value = hash_hmac(content=email, key=config.BLIND_INDEX_HMAC_KEY)

    existing = (
        session.query(PersonsT)
        .filter(PersonsT.blind_index_email == blind_index_email_value)
        .first()
    )

    if existing:
        log.info(f"Person already exists, returning existing record: '{existing.id}'...")
        return Person(id=existing.id)

    person = PersonsT(
        encrypted_email=encrypt(content=email),
        encrypted_first_name=encrypt(content=first_name),
        encrypted_last_name=encrypt(last_name),
        blind_index_email=blind_index_email_value
    )

    try:
        # Creating savepoint to avoid race condition, but to not roll back ALL changes
        nested = session.begin_nested()
        session.add(person)
        session.flush()

    except IntegrityError:
        nested.rollback()
        log.info("Concurrent insert detected, fetching existing Person record...")

        existing = (
            session.query(PersonsT)
            .filter(PersonsT.blind_index_email == blind_index_email_value)
            .first()
        )

        if existing is None:
            raise ValueError(f"Failed to create or retrieve person with email: {email}")
        return Person(id=existing.id)

    log.debug(f"Created new Person with id: '{person.id}...'")
    return Person(id=person.id)