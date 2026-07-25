from sqlalchemy import create_engine
import pytest

from database.schemas import Base, ApiKeys, Users, Persons
from fastapi.testclient import TestClient

@pytest.fixture
def app():
    from main import app
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_db_engine():
    """Create a temporary SQLite database with tables."""
    db_url = "sqlite:///:memory:"
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


