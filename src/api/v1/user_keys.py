from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from auth.dep_verify_user import depends_verify_user, VerifiedUser
from database.session import get_db_session
from database.providers import UserProviderRegistry, get_all_provider_configurations
from database.user_keys import get_or_store_key
from iom.user_keys import PayloadUserKeys, ResponseUserKey
from security.encryption import encrypt


router = APIRouter()


@router.post(
    path="/settings/user/keys",
    tags=["User Settings"],
    description="Stores and returns a User provided Provider API Key.",
    response_model=ResponseUserKey
)
def store_user_key(
    payload: PayloadUserKeys,
    session: Session = Depends(get_db_session),
    user: VerifiedUser = Depends(depends_verify_user)
) -> ResponseUserKey:

    p: UserProviderRegistry = get_all_provider_configurations(
        session=session,
        user_id=user.id
    )

    if payload.provider in p.not_configured:
        sk = get_or_store_key(
            session=session,
            api_key=encrypt(payload.api_key),
            user_id=user.id,
            provider_id=p[payload.provider].id
        )

        return ResponseUserKey(
            user_id=user.id,
            provider=p[payload.provider].name,
            api_key_short=sk.api_key_short,
            expires=sk.expiration_date
        )

    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=f"No keys can be configured for Provider '{payload.provider}'"
    )