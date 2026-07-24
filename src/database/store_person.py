from sqlalchemy.orm import Session

from core.logging import get_logger
from database.schemas import Persons

log = get_logger()

# TODO: Create tests

def store_person(
    session: Session,
    first_name: str,
    last_name: str,
    email: str
) -> None:

    if session.query(Persons).filter(Persons.email == email).count() == 1:
        raise ValueError("Person already exists, skipping...")

    person = Persons(
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    session.add(person)
    session.flush()

    log.info(f"Created new Person with id: {person.id}")

    return person.id