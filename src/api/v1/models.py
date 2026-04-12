from fastapi import APIRouter

from core.config import config
from models.m_models import ReturnAllModels, ReturnTranslationModelsServerLayout, ReturnVecterEmbeddingsServerLayout, ReturnLLMServerLayout

router = APIRouter()
tags = ["Models"]

@router.get(
    "/models",
    tags=tags,
    response_model=ReturnAllModels
)
def get_all_models():
    return {
        "detail": "Success",
        "servers": config.get_model_configuration
    }

@router.get(
    "/models/translation-models",
    tags=["Models", "Translations"],
    response_model=ReturnTranslationModelsServerLayout
)
def get_translation_models():
    return {
        "detail": "Success",
        "servers": config.get_model_configuration
    }

@router.get(
    "/models/vector-embeddings",
    tags=["Models", "Vector Embeddings"],
    response_model=ReturnVecterEmbeddingsServerLayout
)
def get_vector_embedding_models():
    return {
        "detail": "Success",
        "servers": config.get_model_configuration
    }

@router.get(
    "/models/llms",
    tags=["Models", "LLMs"],
    response_model=ReturnLLMServerLayout
)
def get_llms():
    return {
        "detail": "Success",
        "servers": config.get_model_configuration
    }