from fastapi import (
    APIRouter,
    Request,
    Response,
    Depends,
    HTTPException,
    status
)
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from auth.dep_verify_user import depends_verify_user, VerifiedUser
from core.cache import cache_key_builder
from core.logging import get_logger
from database.session import get_db_session
from iom.models import ResponseProviderModels
from providers.models import get_all_models


log = get_logger()


router = APIRouter()


@router.get(
    "/providers/models",
    tags=["Providers"],
    response_model=ResponseProviderModels,
    description="Returns a list of available models, divided by Provider and model expertise."
)
@cache(expire=300, key_builder=cache_key_builder)
async def get_models(
    request: Request,
    response: Response,
    user: VerifiedUser = Depends(depends_verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseProviderModels:

    pm = await get_all_models(
        session=session,
        user_id=user.id
    )

    if pm == {}:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No models available"
        )

    return ResponseProviderModels(
        providers=pm
    )