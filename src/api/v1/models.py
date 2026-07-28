from fastapi import APIRouter, Request, Response, Depends
from fastapi_cache.decorator import cache

from auth.user import verify_user, VerifiedUser
from core.cache import cache_key_builder
from core.logging import get_logger
from io_models.models import (
    ResponseProviderModelsAll,
    ResponseProviderModelsChatCompletions,
    ResponseProviderModelsTranslation,
    ResponseProviderModelsVectorEmbedding
)
from providers.general import _get_all_models

log = get_logger()

router = APIRouter()

@router.get(
    "/models",
    tags=["Models"],
    response_model=ResponseProviderModelsAll
)
@cache(expire=300, key_builder=cache_key_builder)
async def get_all_models(
    request: Request,
    response: Response,
    user: VerifiedUser = Depends(verify_user)
) -> ResponseProviderModelsAll:
    
    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }


@router.get(
    "/models/chat_completion",
    tags=["Models", "Chat Completion"],
    response_model=ResponseProviderModelsChatCompletions
)
@cache(expire=300, key_builder=cache_key_builder)
async def get_all_models_chat_completion(
    request: Request,
    response: Response,
    user: VerifiedUser = Depends(verify_user)
) -> ResponseProviderModelsChatCompletions:
    
    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }


@router.get(
    "/models/translation",
    tags=["Models", "Translation"],
    response_model=ResponseProviderModelsTranslation
)
@cache(expire=300, key_builder=cache_key_builder)
async def get_all_models_translation(
    request: Request,
    response: Response,
    user: VerifiedUser = Depends(verify_user)
) -> ResponseProviderModelsTranslation:

    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }


@router.get(
    "/models/vector_embedding",
    tags=["Models", "Vector Embedding"],
    response_model=ResponseProviderModelsVectorEmbedding
)
@cache(expire=300, key_builder=cache_key_builder)
async def get_all_models_vector_embedding(
    request: Request,
    response: Response,
    user: VerifiedUser = Depends(verify_user)
) -> ResponseProviderModelsVectorEmbedding:

    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }