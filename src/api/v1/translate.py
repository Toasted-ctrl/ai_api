import requests

from fastapi import APIRouter, HTTPException, status

from core.config import config
from models.m_translate import ReturnTranslationModels
from ollama_server.models import get_translators, get_models

router = APIRouter()
tags = ["Translation"]

@router.get(
    "/translate",
    tags=tags,
    response_model=ReturnTranslationModels
)
def get_translation_models():
    try:
        models = get_models(base_url=config.OLLAMA_BASE_URL)
        if not models:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No models"
            )
        
        translation_models = get_translators(models=models)
        if not translation_models:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No translation models"
            )

        return {
            "detail": "Success",
            "models": translation_models
        }

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not connect to Ollama server")
    
# TODO: Implement post translation request endpoint