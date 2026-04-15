from fastapi import APIRouter

from core.config import config
from models.m_translations import PayloadTranslation, ReturnTranslation
from model_servers.ollama.translations import get_translation_translategemma

router = APIRouter()
tags = ["Translations"]

# TODO: Build test for the below endpoint.

@router.post(
    "/translations",
    tags=tags,
    response_model=ReturnTranslation
)
def get_translation(payload: PayloadTranslation):
    translation = get_translation_translategemma(
        from_language=payload.from_language,
        from_lang_code=payload.from_lang_code,
        to_language=payload.to_language,
        to_lang_code=payload.to_lang_code,
        query=payload.query,
        server_url=config.OLLAMA_BASE_URL,
        temperature=payload.temperature
    )

    return {
        "detail": "Success",
        "translation": translation
    }