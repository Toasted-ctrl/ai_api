from sqlalchemy import text

from database.session import get_db_session

def test_get_db_yields_session():
    with get_db_session("sqlite:///:memory:") as session:
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1