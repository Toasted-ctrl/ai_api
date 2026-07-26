from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import uuid

from core.logging import get_logger
from database.schemas import Persons

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

    existing = session.query(Persons).filter(Persons.email == email).first()
    if existing:
        log.info("Person already exists, returning existing record...")
        return StoredPerson(id=existing.id)

    person = Persons(
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    try:
        # Creating savepoint to avoid race condition, but to not roll back ALL changes
        nested = session.begin_nested()
        session.add(person)
        session.flush()
    except IntegrityError:
        nested.rollback()
        log.info("Concurrent insert detected, fetching existing Person record...")
        existing = session.query(Persons).filter(Persons.email == email).first()
        if existing is None:
            raise ValueError(f"Failed to create or retrieve person with email: {email}")
        return StoredPerson(id=existing.id)

    log.info(f"Created new Person with id: {person.id}")
    return StoredPerson(id=person.id)