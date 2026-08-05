from fastapi import (
    HTTPException,
    status,
    APIRouter,
    Depends,
    Request,
    Response
)
from fastapi_cache.decorator import cache
from httpx import ConnectError, ConnectTimeout
from sqlalchemy.orm import Session

from auth.user import verify_user, VerifiedUser
from core.cache import cache_key_builder
from database.providers import get_provider, Provider
from database.session import get_db_session
from io_models.translations import (
    ResponseTranslation,
    PayloadTranslation,
    ResponseTranslationLanguages
)
from providers.ollama.translategemma import (
    translategemma_languages,
    get_translation_translategemma
)
from providers.general import find_provider, get_all_models

router = APIRouter()

tags = ["Translation"]


@router.post(
    "/translation/translategemma",
    tags=tags,
    description="Invokes a translation from translategemma",
    response_model=ResponseTranslation
)
async def post_translation_translategemma(
    payload: PayloadTranslation,
    user: VerifiedUser = Depends(verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseTranslation:

    try:

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

        provider_name = find_provider(
            data=await get_all_models(session=session),
            model_name="translategemma:latest"
        )
        if provider_name is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Translategemma is unavailable"
            )

        provider: Provider = get_provider(
            session=session,
            provider_name=provider_name
        )
        if provider is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unexpected Error: Could not locate Provider"
            )
        
        return get_translation_translategemma(
            from_lang=payload.from_lang_code,
            to_lang=payload.to_lang_code,
            prompt=payload.prompt,
            temperature=payload.parameters.temperature,
            base_url=provider.base_url
        )

    except (ConnectTimeout, ConnectError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Provider"
        )
    

@router.get(
    "/translation/translategemma",
    tags=["Translation"],
    response_model=ResponseTranslationLanguages,
    description="Returns languages supported by translategemma."
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