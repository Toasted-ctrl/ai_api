from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pytest

from auth.hash import get_hash_sha356
from database.store_secrets import store_secrets
from database.schemas import ApiKeys, Base

@pytest.fixture
def test_db():
    """Create a temporary SQLite database with tables."""
    db_url = "sqlite:///:memory:"
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


class TestCreateApiKey:

    """Test battery for the create_api_key function."""

    def test_valid(self, test_db):
        with Session(bind=test_db) as session:
            secrets = store_secrets(
                db=session,
                client="test_client",
                key_type="User",
                owner_email="test_mail"
            )
            session.commit()

            assert (
                session.query(ApiKeys)
                .filter(ApiKeys.api_key_hash == get_hash_sha356(secrets.get('client_api_key')))
                .count()
            ) == 1


    def test_duplicate_key(self, test_db):
        with Session(bind=test_db) as session:
            test_client = "test_client"
            secrets = store_secrets(
                db=session,
                client=test_client,
                key_type="User",
                owner_email="test_mail"
            )
            session.commit()
            with pytest.raises(
                ValueError,
                match=f"Client '{test_client}' with owner 'test_mail' already exists"
            ):
                secrets2 = store_secrets(
                    db=session,
                    client=test_client,
                    key_type="User",
                    owner_email="test_mail"
                )
                session.commit()