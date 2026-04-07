from fastapi import APIRouter, HTTPException, status

from core.config import config
from models.m_translate import PayloadTranslation, ReturnTranslation, ReturnTranslationModels
from ollama_server.models import get_translation_models
from ollama_server.server_status import is_ollama_server_online

router = APIRouter()
tags = ["Translation"]

@router.get(
    "/translate",
    tags=tags,
    response_model=ReturnTranslationModels)
def get_translation_models():
    if not is_ollama_server_online(base_url=config.OLLAMA_BASE_URL) is True:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ollama server offline"
        )
    
    models = get_translation_models(base_url=config.OLLAMA_BASE_URL)
    if not models:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Translation model(s) offline"
        )
    
    return {
        "detail": "Success",
        "models": models
    }

@router.post(
    "/translate",
    tags=tags,
    response_model=ReturnTranslation)
def post_translation_request(payload: PayloadTranslation):

    if not is_ollama_server_online(base_url=config.OLLAMA_BASE_URL) is True:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ollama server offline") # TODO: Build test for this part.

    # TODO: Langchain and Langchain Ollama required.
    # TODO: Add it to a new directory in source.
    # TODO: Create check to verify that the requested model is online.

    return {
        "detail": "Success",
        "from_language": "test_from",
        "to_language": "test_to",
        "text_input": "test_input",
        "text_output": "test_output"
    }