from fastapi import (
    HTTPException,
    status,
    APIRouter,
    Depends,
    Request,
    Response
)
from fastapi_cache.decorator import cache

from auth.user import verify_user, VerifiedUser
from core.cache import cache_key_builder
from io_models.translations import (
    ResponseTranslation,
    PayloadTranslation,
    ResponseTranslationLanguages
)
from providers.ollama.translategemma import (
    translategemma_locate,
    translategemma_languages,
    get_translation_translategemma
)

router = APIRouter()

tags = ["Translation"]

@router.post(
    "/translation/translategemma",
    tags=tags,
    response_model=ResponseTranslation
)
def post_translation_translategemma(
    payload: PayloadTranslation,
    user: VerifiedUser = Depends(verify_user)
) -> ResponseTranslation:

    if payload.from_lang_code not in translategemma_languages():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported language: {payload.from_lang_code}"
        )
    
    if payload.to_lang_code not in translategemma_languages():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported language: {payload.to_lang_code}"
        )
    
    if payload.prompt == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt must not be None"
        )

    host = translategemma_locate()
    if host is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Translategemma is unavailable"
        )
    
    return get_translation_translategemma(
        from_lang=payload.from_lang_code,
        to_lang=payload.to_lang_code,
        prompt=payload.prompt,
        temperature=payload.parameters.temperature,
        host=host
    )


@router.get(
    "/translation/translategemma",
    tags=["Translation"],
    response_model=ResponseTranslationLanguages
)
@cache(
    expire=300,
    key_builder=cache_key_builder
)
def get_languages_translategemma(
    request: Request,
    response: Response,
    user: VerifiedUser = Depends(verify_user)
) -> ResponseTranslationLanguages:
    
    return {
        "languages": translategemma_languages()
    }