from fastapi import (
    APIRouter,
    Depends
)
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from auth.user import verify_user, VerifiedUser
from core.cache import cache_key_builder
from database.providers import get_all_providers_support_user
from database.session import get_db_session
from io_models.providers import ProvidersResponse

router = APIRouter(prefix='/providers')

tags = ["Providers"]


@router.get(
    "",
    response_model=ProvidersResponse,
    description=(
        "Returns a list of Providers that are available through the API. "
        "Provides an indication of whether a User-provided Provider API key is required, "
        "and if a Provider API key has been configured."
    ),
    tags=tags
)
@cache(expire=600, key_builder=cache_key_builder)
async def get_all_providers(
    user: VerifiedUser = Depends(verify_user),
    session: Session = Depends(get_db_session)
) -> ProvidersResponse:

    # TODO: In the future, add which api_key_ids the user has access to.

    providers = get_all_providers_support_user(
        session=session
    )

    return {
        "providers": providers
    }