from core.config import config


def test_db_url():

    assert isinstance(config.PG_DB_URL, str)