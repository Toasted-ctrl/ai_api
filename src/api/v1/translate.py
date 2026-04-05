from fastapi import APIRouter, HTTPException, status

from core.config import config
from models.m_translate import PayloadTranslation, ReturnTranslation
from ollama.server_status import is_ollama_server_online

router = APIRouter()
tags = ["Translation"]

@router.post(
    "/translate",
    tags=tags,
    response_model=ReturnTranslation)
def post_translation_request(payload: PayloadTranslation):

    if is_ollama_server_online(base_url=config.OLLAMA_BASE_URL) is False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="LLM server offline") # TODO: Build test for this part.

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