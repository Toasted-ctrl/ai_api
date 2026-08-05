from sqlalchemy.orm import Session
import pytest
import uuid

from database.schemas.persons_users import UsersT
from database.user import get_or_store_user

class TestStoreUser:

    """Test suite for store_user() function."""

    def test_valid(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            user = get_or_store_user(
                session=session,
                person_id=uuid.uuid4(),
                api_key_id=uuid.uuid4(),
                key_type="User"
            )
            assert isinstance(user.id, uuid.UUID)

            session.close()


    def test_duplicate_user(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            person_id = uuid.uuid4()
            api_key_id = uuid.uuid4()
            key_type = "User"

            get_or_store_user(
                session=session,
                person_id=person_id,
                api_key_id=api_key_id,
                key_type=key_type
            )

            get_or_store_user(
                session=session,
                person_id=person_id,
                api_key_id=api_key_id,
                key_type=key_type
            )

            count = (
                session.query(UsersT).count()
            )

            assert count == 1

            session.close()


    def test_missing_external_id(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            with pytest.raises(
                ValueError,
                match="Unable to fetch or add User, if key_type = 'Application', external_id must not be None"
            ):

                get_or_store_user(
                    session=session,
                    person_id=uuid.uuid4(),
                    api_key_id=uuid.uuid4(),
                    key_type="Application"
                )

            session.close()