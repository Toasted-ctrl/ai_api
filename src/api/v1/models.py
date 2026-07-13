from fastapi import APIRouter
from fastapi_cache.decorator import cache

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
@cache(expire=120)
async def get_all_models():
    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }


@router.get(
    "/models/chat_completion",
    tags=["Models", "Chat Completion"],
    response_model=ResponseProviderModelsChatCompletions
)
@cache(expire=120)
async def get_all_models_chat_completion():
    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }


@router.get(
    "/models/translation",
    tags=["Models", "Translation"],
    response_model=ResponseProviderModelsTranslation
)
@cache(expire=120)
async def get_all_models_translation():
    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }


@router.get(
    "/models/vector_embedding",
    tags=["Models", "Vector Embedding"],
    response_model=ResponseProviderModelsVectorEmbedding
)
@cache(expire=120)
async def get_all_models_vector_embedding():
    log.debug("Result cached")
    return {
        "provider": await _get_all_models()
    }