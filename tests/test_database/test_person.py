from sqlalchemy.orm import Session
import uuid

from database.person import get_or_store_person, StoredPerson
from database.schemas import Persons

class TestGetOrStorePerson:

    """Test battery for the get_or_store_person() function."""

    def test_valid(self, test_db_engine):

        with Session(bind=test_db_engine) as session:

            person = get_or_store_person(
                session=session,
                first_name="test_first_name",
                last_name="test_last_name",
                email="test_email")

            assert person is not None
            assert isinstance(person, StoredPerson)
            assert isinstance(person.id, uuid.UUID)


    def test_duplicate(self, test_db_engine):

        with Session(bind=test_db_engine) as session:

            get_or_store_person(
                session=session,
                first_name="test_first_name",
                last_name="test_last_name",
                email="test_email"
            )

            _person = get_or_store_person(
                session=session,
                first_name="test_first_name",
                last_name="test_last_name",
                email="test_email"
            )

            assert session.query(Persons).filter(Persons.email == "test_email").count() == 1
            assert isinstance(_person, StoredPerson)
            assert isinstance(_person.id, uuid.UUID)