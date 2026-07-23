from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pytest

from database.api_key import create_api_key
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
            key = create_api_key(
                db=session,
                client="test_client"
            )
            session.commit()
            assert session.query(ApiKeys).filter(ApiKeys.api_key == key).count() == 1


    def test_duplicate_key(self, test_db):
        with Session(bind=test_db) as session:
            test_client = "test_client"
            key = create_api_key(
                db=session,
                client=test_client
            )
            session.commit()
            with pytest.raises(
                ValueError,
                match=f"Client '{test_client}' already exists"
            ):
                key2 = create_api_key(
                    db=session,
                    client=test_client
                )
                session.commit()