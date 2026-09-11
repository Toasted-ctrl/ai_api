from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from fastapi import HTTPException, status, Depends, Cookie
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.orm import Session
from warnings import deprecated
import uuid

from auth.dep_verify_client import VerifiedClient, depends_get_client
from core.logging import get_logger
from database.schemas.persons_users import UsersT
from database.schemas.user_sessions import SessionsT
from database.session import get_db_session
from security.hash import get_hash_sha256


log = get_logger()


class KeyType(str, Enum):
    APPLICATION = "Application"
    USER = "User"


@dataclass(frozen=True)
class VerifiedUser:
    id: uuid.UUID


def depends_verify_user(
    client: VerifiedClient = Depends(depends_get_client),
    session: Session = Depends(get_db_session),
    session_id: str | None = Cookie(default=None)
) -> VerifiedUser:
    """Resolved a VerifiedClient to a VerifiedUser.
    Returns VerifiedUser if valid, otherwise raises HTTPException."""

    kt: KeyType = client.key_type

    match kt:
        case KeyType.APPLICATION:
            if not session_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing session cookie"
                )

            user = (
                session.query(SessionsT)
                .filter(
                    SessionsT.session_id_hash == get_hash_sha256(session_id),
                    SessionsT.expiration_date > datetime.now(timezone.utc)
                )
                .one_or_none()
            )

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired session"
                )

            client_id_check = (
                session.query(UsersT)
                .filter(
                    UsersT.api_key_id == client.id,
                    UsersT.id == user.user_id
                )
                .one_or_none()
            )

            if client_id_check is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User is not authorized"
                )

            log.debug(f"Verified User: {user.user_id}")
            return VerifiedUser(
                id=user.user_id
            )

        case KeyType.USER:
            try:
                user = session.query(UsersT).filter(UsersT.api_key_id == client.id).one_or_none()
            except MultipleResultsFound:
                log.critical(f"Multiple Users found for api_key_id: {client.id}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unexpected error. Please contact your administrator."
                )

            log.debug(f"Verified User: {user.id}")
            return VerifiedUser(
                id=user.id
            )

        case _:
            log.error(f"Invalid key_type: {client.key_type}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error. Please contact your administrator."
            )