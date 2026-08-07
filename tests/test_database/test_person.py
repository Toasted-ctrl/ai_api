from sqlalchemy.orm import Session
import uuid

from core.config import config
from database.person import get_or_store_person, Person
from database.schemas.persons_users import PersonsT
from security.hmac import hash_hmac

class TestGetOrStorePerson:

    """Test battery for the get_or_store_person() function."""

    # -------------------------------------------------------------------
    # Happy-path tests
    # -------------------------------------------------------------------
    

    def test_valid(self, test_db_engine):

        with Session(bind=test_db_engine) as session:

            person = get_or_store_person(
                session=session,
                first_name="test_first_name",
                last_name="test_last_name",
                email="test_email")

            assert person is not None
            assert isinstance(person, Person)
            assert isinstance(person.id, uuid.UUID)


    def test_duplicate(self, test_db_engine):

        with Session(bind=test_db_engine) as session:

            email = "Test Email"
            first_name = "Test First Name"
            last_name = "Test Last Name"

            get_or_store_person(
                session=session,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            _person = get_or_store_person(
                session=session,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            assert (
                session.query(PersonsT)
                .filter(PersonsT.blind_index_email == hash_hmac(content=email, key=config.BLIND_INDEX_HMAC_KEY))
                .count()
            ) == 1

            assert isinstance(_person, Person)
            assert isinstance(_person.id, uuid.UUID)