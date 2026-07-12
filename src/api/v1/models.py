from fastapi import APIRouter

from io_models.models import (
    ResponseProviderModelsAll,
    ResponseProviderModelsChatCompletions,
    ResponseProviderModelsTranslation,
    ResponseProviderModelsVectorEmbedding
)
from providers.general import _get_all_models

router = APIRouter()

@router.get(
    "/models",
    tags=["Models"],
    response_model=ResponseProviderModelsAll
)
def get_all_models():
    return {
        "provider": _get_all_models()
    }


@router.get(
    "/models/chat_completion",
    tags=["Models", "Chat Completion"],
    response_model=ResponseProviderModelsChatCompletions
)
def get_all_models_chat_completion():
    return {
        "provider": _get_all_models()
    }


@router.get(
    "/models/translation",
    tags=["Models", "Translation"],
    response_model=ResponseProviderModelsTranslation
)
def get_all_models_translation():
    return {
        "provider": _get_all_models()
    }


@router.get(
    "/models/vector_embedding",
    tags=["Models", "Vector Embedding"],
    response_model=ResponseProviderModelsVectorEmbedding
)
def get_all_models_vector_embedding():
    return {
        "provider": _get_all_models()
    }