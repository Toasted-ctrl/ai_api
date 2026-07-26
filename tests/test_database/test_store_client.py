from sqlalchemy.orm import Session
import pytest

from auth.hash import get_hash_sha256
from database.store_client import store_client
from database.schemas import ApiKeys

class TestCreateApiKey:

    """Test battery for the create_api_key function."""

    def test_valid(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            _client = store_client(
                session=session,
                client="test_client",
                key_type="User",
                owner_email="test_mail"
            )
            session.commit()

            assert (
                session.query(ApiKeys)
                .filter(ApiKeys.api_key_hash == get_hash_sha256(_client.api_key))
                .count()
            ) == 1

            session.close()


    def test_duplicate_key(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            test_client = "test_client"
            secrets = store_client(
                session=session,
                client=test_client,
                key_type="User",
                owner_email="test_mail"
            )
            session.commit()
            with pytest.raises(
                ValueError,
                match=f"Client '{test_client}' with owner 'test_mail' already exists"
            ):
                secrets2 = store_client(
                    session=session,
                    client=test_client,
                    key_type="User",
                    owner_email="test_mail"
                )
                session.commit()
            session.close()