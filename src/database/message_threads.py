from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import uuid

from core.logging import get_logger
from database.schemas.message_threads import MessageThreadsT

log = get_logger()


def store_thread_id(
    session: Session,
    thread_id: uuid.UUID,
    user_id: uuid.UUID
) -> uuid.UUID:
    """Stores and returns the thread_id generated for a conversation."""

    log.debug(f"Storing thread_id '{thread_id}' for user '{user_id}' ...")

    ntid = MessageThreadsT(
        id=thread_id,
        user_id=user_id
    )

    session.add(ntid)
    session.flush()

    log.debug(f"Thread_id '{ntid.id}' stored, returning ...")

    return ntid.id


def verify_or_get_thread_id(
    session: Session,
    user_id: uuid.UUID,
    thread_id: uuid.UUID | None = None
) -> uuid.UUID:
    """Searcheds for and returns the thread_id if it belongs to the user_id.
    Will raise a HTTPException if the thread_id does not belong to the user_id.
    Creates and stores a new threa_id if the passed threa_id is None."""

    if thread_id:
        id = (
            session.query(MessageThreadsT.id)
            .filter(
                MessageThreadsT.user_id == user_id,
                MessageThreadsT.id == thread_id
            )
            .scalar()
        )

        if id:
            return id
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid thread_id"
            )

    else:
        ntid = uuid.uuid4()
        return store_thread_id(
            session=session,
            thread_id=ntid,
            user_id=user_id
        )