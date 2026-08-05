from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from httpx import ConnectTimeout, ConnectError
from sqlalchemy.orm import Session

from auth.user import verify_user, VerifiedUser
from core.logging import get_logger
from database.providers import get_all_providers_support_user, Provider
from database.session import get_db_session
from io_models.chat_completion import PayloadChatCompletion
from providers.general import get_all_models
from providers.ollama.chat_completion import complete_chat_ollama

router = APIRouter()

log = get_logger()


@router.post(
    "/chat_completion",
    tags=["Chat Completion"],
    response_class=StreamingResponse
)
async def post_chat_completion(
    payload: PayloadChatCompletion,
    user: VerifiedUser = Depends(verify_user),
    session: Session = Depends(get_db_session)
) -> StreamingResponse:

    try:

        # TODO: Add API Key check to based on user.

        providers = get_all_providers_support_user(
            session=session
        )

        provider_list = [
            p.name for p in providers if p.internal or p.api_key_configured
        ]

        provider: Provider = [p for p in providers if p.name == payload.provider][0]

        if payload.provider not in provider_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported or unconfigured Provider"
            )

        models = await get_all_models(
            session=session
        )

        if payload.model not in models.get(payload.provider).get("chat_completion"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model not supported by Provider"
            )

        return StreamingResponse(
            complete_chat_ollama(
                prompt=payload.prompt,
                url=provider.base_url,
                model=payload.model,
                stream=payload.stream,
                temperature=payload.parameters.temperature,
                top_k=payload.parameters.top_k,
                top_p=payload.parameters.top_p
            )
        )

    except (ConnectTimeout, ConnectError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Provider"
        )