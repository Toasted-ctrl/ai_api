import requests

from fastapi import APIRouter, HTTPException, status

from core.config import config
from models.m_models import ReturnModels
from ollama_server.models import get_models

router = APIRouter()
tags = ["Models"]

@router.get(
    "/models",
    tags=tags,
    response_model=ReturnModels
)
def get_all_models():
    try:
        models = get_models(base_url=config.OLLAMA_BASE_URL)
        if not models:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No models"
            )
        
        allowed_keys = ["name", "size"]
        return {
            "detail": "Success",
            "models": [{k: v for k, v in model.items() if k in allowed_keys} for model in models]
        }

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not connect to Ollama server"
        )