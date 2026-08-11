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

from core.cache import cache_key_builder
from database.providers import ProviderConfiguration
from database.session import get_db_session
from dependencies.d_v_user import dep_ver_usr, VerifiedUser
from io_models.translations import (
    ResponseTranslation,
    PayloadTranslation,
    ResponseTranslationLanguages
)
from providers.ollama.translategemma import (
    translategemma_languages,
    get_translation_translategemma
)
from providers.models import get_all_provider_configurations

router = APIRouter()

tags = ["Translation"]


@router.post(
    "/translation/translategemma",
    tags=tags,
    description="Invokes a translation from translategemma.",
    response_model=ResponseTranslation
)
async def post_translation_translategemma(
    payload: PayloadTranslation,
    user: VerifiedUser = Depends(dep_ver_usr),
    session: Session = Depends(get_db_session)
) -> ResponseTranslation:

    try:

        if not {payload.to_lang_code, payload.from_lang_code} <= translategemma_languages():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported language: {payload.from_lang_code}"
            )
        
        if payload.prompt == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt must not be None"
            )

        p = "Ollama-1"

        # Default provider for now? Perhaps we can fetch all providers by 
        # Langchain con instead? Cache the result?
        # TODO: Find a way to pinpoint the correct provider.

        providers = get_all_provider_configurations(
            session=session,
            user_id=user.id
        )

        provider: ProviderConfiguration = providers.get(p)
        
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
    user: VerifiedUser = Depends(dep_ver_usr)
) -> ResponseTranslationLanguages:
    
    return {
        "languages": translategemma_languages()
    }