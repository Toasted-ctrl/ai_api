from collections.abc import Generator
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import config
from core.logging import get_logger

log = get_logger()

engine = create_engine(
    url=config.PG_DB_URL,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

def get_db_session() -> Generator[Session]:
    """FastAPI dependency that yields a database session."""
    log.info("Opening database session")
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        log.info("Closed database session")


@contextmanager
def get_db_session_ctx() -> Generator[Session]:
    """For use outside of FastAPI (scripts, workers, etc.)."""
    log.debug("Opening database session")
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        log.debug("Closed database session")