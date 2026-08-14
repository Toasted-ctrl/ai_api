from dataclasses import dataclass
from fastapi import HTTPException, status, Depends
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.orm import Session
import uuid

from auth.dep_verify_client import VerifiedClient, depends_get_client
from core.logging import get_logger
from database.schemas.persons_users import UsersT
from database.session import get_db_session

log = get_logger()


@dataclass(frozen=True)
class VerifiedUser:
    id: uuid.UUID


def depends_verify_user(
    client: VerifiedClient = Depends(depends_get_client),
    session: Session = Depends(get_db_session)
) -> VerifiedUser:

    """Resolved a VerifiedClient to a VerifiedUser.
    Returns VerifiedUser if valid, otherwise raises HTTPException."""

    if client.key_type == "Application":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Application key JWT decoding not yet supported"
        )

    if client.key_type != "User":
        log.error(f"Invalid key_type: {client.key_type}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error. Please contact your administrator."
        )

    try:
        user = session.query(UsersT).filter(UsersT.api_key_id == client.id).one_or_none()
    except MultipleResultsFound:
        log.critical(f"Multiple Users found for api_key_id: {client.id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error. Please contact your administrator."
        )

    if not user:
        log.warning(f"No User found for api_key_id: {client.id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )

    log.debug(f"Verified User: {user.id}")
    return VerifiedUser(
        id=user.id
    )