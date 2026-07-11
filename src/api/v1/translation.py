from fastapi import APIRouter, HTTPException, status

from core.config import config
from io_models.translations import ResponseTranslation, PostTranslation
from providers.ollama.translategemma import supported_languages as translategemma_languages
from providers.ollama.translations import get_translation_translategemma

router = APIRouter()
tags = ["Translations"]

@router.post(
    "/models/translations",
    tags=tags,
    response_model=ResponseTranslation
)
def post_translation(payload: PostTranslation):

    if payload.provider not in config.SUPPORTED_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Unsupported Provider: '{payload.provider}'"
        )
    
    if payload.provider == 'Ollama-1':

        if payload.model == 'translategemma:latest':

            supported_languages = translategemma_languages()
            if payload.to_lang_code not in supported_languages:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported language: '{payload.to_lang_code}'"
                )
            if payload.from_lang_code not in supported_languages:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported language: '{payload.from_lang_code}'"
                )

            translation = get_translation_translategemma(
                from_lang=payload.from_lang_code,
                to_lang=payload.to_lang_code,
                prompt=payload.prompt,
                temperature=payload.parameters.temperature
            )

            return translation
    
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported Model: '{payload.model}'"
            )