from fastapi import APIRouter, Request, Response, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from auth.user import verify_user, VerifiedUser
from core.cache import cache_key_builder
from core.logging import get_logger
from database.session import get_db_session
from io_models.models import (
    ResponseProviderModelsAll,
    ResponseProviderModelsChatCompletions,
    ResponseProviderModelsTranslation,
    ResponseProviderModelsVectorEmbedding
)
from providers.general import get_all_models

log = get_logger()

router = APIRouter()


@router.get(
    "/models",
    tags=["Models"],
    response_model=ResponseProviderModelsAll
)
@cache(expire=300, key_builder=cache_key_builder)
async def get_all(
    request: Request,
    response: Response,
    user: VerifiedUser = Depends(verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseProviderModelsAll:

    provider_models = await get_all_models(
        session=session,
        user_id=user.id
    )

    if provider_models == {}:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No models available"
        )
    
    return {
        "providers": provider_models
    }


@router.get(
    "/models/chat_completion",
    tags=["Models", "Chat Completion"],
    response_model=ResponseProviderModelsChatCompletions
)
@cache(expire=300, key_builder=cache_key_builder)
async def get_all_chat_completion(
    request: Request,
    response: Response,
    user: VerifiedUser = Depends(verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseProviderModelsChatCompletions:
    
    provider_models = await get_all_models(
        session=session,
        user_id=user.id
    )

    if provider_models == {}:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No models available"
        )
        
    return {
        "providers": provider_models
    }


@router.get(
    "/models/translation",
    tags=["Models", "Translation"],
    response_model=ResponseProviderModelsTranslation
)
@cache(expire=300, key_builder=cache_key_builder)
async def get_all_translation(
    request: Request,
    response: Response,
    user: VerifiedUser = Depends(verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseProviderModelsTranslation:

    provider_models = await get_all_models(
        session=session,
        user_id=user.id
    )

    if provider_models == {}:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No models available"
        )
        
    return {
        "providers": provider_models
    }


@router.get(
    "/models/vector_embedding",
    tags=["Models", "Vector Embedding"],
    response_model=ResponseProviderModelsVectorEmbedding
)
@cache(expire=300, key_builder=cache_key_builder)
async def get_all_vector_embedding(
    request: Request,
    response: Response,
    user: VerifiedUser = Depends(verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseProviderModelsVectorEmbedding:

    provider_models = await get_all_models(
        session=session,
        user_id=user.id
    )

    if provider_models == {}:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No models available"
        )
        
    return {
        "providers": provider_models
    }