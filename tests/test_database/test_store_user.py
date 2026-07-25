from sqlalchemy.orm import Session
import pytest
import uuid

from database.store_user import store_user

class TestStoreUser:

    """Test battery for test_store_user() function."""

    def test_valid(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            user = store_user(
                session=session,
                person_id=uuid.uuid4(),
                api_key_id=uuid.uuid4(),
                key_type="User"
            )
            assert isinstance(user, uuid.UUID)

            session.close()


    def test_duplicate_user(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            person_id = uuid.uuid4()
            api_key_id = uuid.uuid4()
            key_type = "User"

            store_user(
                session=session,
                person_id=person_id,
                api_key_id=api_key_id,
                key_type=key_type
            )

            with pytest.raises(
                ValueError,
                match="User already exists, skipping..."
            ):

                store_user(
                    session=session,
                    person_id=person_id,
                    api_key_id=api_key_id,
                    key_type=key_type
                )

            session.close()


    def test_missing_external_id(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            with pytest.raises(
                ValueError,
                match="Unable to add User, if key_type = 'Application', external_id must not be None"
            ):

                store_user(
                    session=session,
                    person_id=uuid.uuid4(),
                    api_key_id=uuid.uuid4(),
                    key_type="Application"
                )

            session.close()