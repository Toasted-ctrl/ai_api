from sqlalchemy import create_engine

from core.config import config
from core.logging import get_logger

# Imported so their tables are registered with Base.metadata
from database.schemas.base import Base
from database.schemas.clients import ClientsT
from database.schemas.persons_users import PersonsT, UsersT
from database.schemas.providers import ProvidersT

log = get_logger()


def create_tables():

    try:
        engine = create_engine(url=config.PG_DB_URL)
        log.info("Created engine to create required tables...")

        Base.metadata.create_all(bind=engine)
        log.info("Created required tables...")

        return

    except Exception as e:
        log.error(f"Unexpected error: {e}. Shutting down...")
        raise SystemExit(1)

    finally:
        if engine:
            engine.dispose()
            log.info("Disposed engine...")