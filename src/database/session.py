from collections.abc import Generator
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
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
        session.commit()
    except ValueError or SQLAlchemyError as e:
        session.rollback()
        log.warning(f"Error while executing database operations: {e} No updates made.")
    except Exception as e:
        session.rollback()
        log.warning(f"Unexpected error occured while performing database operations: {e}, Rolling back updates.")
    finally:
        session.close()
        log.debug("Closed database session")
        engine.dispose()
        log.debug("Disposed database engine")