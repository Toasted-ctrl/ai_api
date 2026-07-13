from fastapi import APIRouter, Request, Response
from fastapi_cache.decorator import cache

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
@cache(expire=120, key_builder=cache_key_builder)
async def get_all_models(request: Request, response: Response):
    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }


@router.get(
    "/models/chat_completion",
    tags=["Models", "Chat Completion"],
    response_model=ResponseProviderModelsChatCompletions
)
@cache(expire=120, key_builder=cache_key_builder)
async def get_all_models_chat_completion(request: Request, response: Response):
    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }


@router.get(
    "/models/translation",
    tags=["Models", "Translation"],
    response_model=ResponseProviderModelsTranslation
)
@cache(expire=120, key_builder=cache_key_builder)
async def get_all_models_translation(request: Request, response: Response):
    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }


@router.get(
    "/models/vector_embedding",
    tags=["Models", "Vector Embedding"],
    response_model=ResponseProviderModelsVectorEmbedding
)
@cache(expire=120, key_builder=cache_key_builder)
async def get_all_models_vector_embedding(request: Request, response: Response):
    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }