from sqlalchemy.orm import Session
import pytest
import uuid

from database.store_person import store_person

class TestStorePerson:

    """Test battery for the store_person() function."""

    def test_valid(self, test_db_engine):

        with Session(bind=test_db_engine) as session:

            person = store_person(
                session=session,
                first_name="test_first_name",
                last_name="test_last_name",
                email="test_email")

            assert person is not None
            assert isinstance(person, uuid.UUID)


    def test_duplicate(self, test_db_engine):

        with Session(bind=test_db_engine) as session:

            store_person(
                session=session,
                first_name="test_first_name",
                last_name="test_last_name",
                email="test_email"
            )

            with pytest.raises(
                ValueError,
                match="Person already exists, skipping..."
            ):

                store_person(
                    session=session,
                    first_name="test_first_name",
                    last_name="test_last_name",
                    email="test_email"
                )