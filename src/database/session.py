from collections.abc import Generator
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.logging import get_logger

log = get_logger()

@contextmanager
def get_db_session(db_url: str) -> Generator[Session]:
    log.debug("Opening database session")
    engine = create_engine(url=db_url, echo=False)
    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        log.debug("Closed database session")
        engine.dispose()
        log.debug("Disposed database engine")