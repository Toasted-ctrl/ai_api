from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import uuid

from core.config import config
from core.logging import get_logger
from database.schemas import Persons
from security.encryption import encrypt
from security.hmac import hash_hmac

log = get_logger()

@dataclass(frozen=True)
class StoredPerson:
    id: uuid.UUID


def get_or_store_person(
    session: Session,
    first_name: str,
    last_name: str,
    email: str
) -> StoredPerson:

    """Stores a new or retrieves an existing person from the database."""

    blind_index_email_value = hash_hmac(content=email, key=config.BLIND_INDEX_HMAC_KEY)

    existing = (
        session.query(Persons)
        .filter(Persons.blind_index_email == blind_index_email_value)
        .first()
    )

    if existing:
        log.info(f"Person already exists, returning existing record: '{existing.id}'...")
        return StoredPerson(id=existing.id)

    person = Persons(
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
            session.query(Persons)
            .filter(Persons.blind_index_email == blind_index_email_value)
            .first()
        )

        if existing is None:
            raise ValueError(f"Failed to create or retrieve person with email: {email}")
        return StoredPerson(id=existing.id)

    log.debug(f"Created new Person with id: '{person.id}...'")
    return StoredPerson(id=person.id)