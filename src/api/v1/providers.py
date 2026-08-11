from fastapi import (
    APIRouter,
    Depends
)
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from core.cache import cache_key_builder
from database.providers import get_all_provider_configurations
from database.session import get_db_session
from dependencies.d_v_user import dep_ver_usr, VerifiedUser
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
    user: VerifiedUser = Depends(dep_ver_usr),
    session: Session = Depends(get_db_session)
) -> ProvidersResponse:

    p_reg = get_all_provider_configurations(
        session=session,
        user_id=user.id
    )

    return {
        "providers": [p for p in p_reg]
    }