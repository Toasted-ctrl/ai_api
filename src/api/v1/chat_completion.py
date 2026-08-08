from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from httpx import ConnectTimeout, ConnectError
from sqlalchemy.orm import Session

from auth.user import verify_user, VerifiedUser
from core.config import config
from core.logging import get_logger
from database.providers import get_all_provider_configurations, ProviderConfiguration
from database.session import get_db_session
from io_models.chat_completion import PayloadChatCompletion
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

        if payload.model not in config.CHAT_COMPLETION_MODELS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model not supported by Provider"
            )

        # TODO: Do we perhaps want to confirm that the model is supported by the provider?

        p_reg = get_all_provider_configurations(
            session=session,
            user_id=user.id
        )

        if payload.provider not in p_reg.names or payload.provider in p_reg.not_configured:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Provider '{payload.provider}' is not supported or not configured"
            )

        prov: ProviderConfiguration = getattr(p_reg, payload.provider)

        # TODO: Currently this works, but we'll need to add support for Melious (OpenAI) and Anthropic as well.
        # Build more general streaming response class and use langchain_con from the provider to determine 
        # which connector to use.
        # Raising error for now if a provider is selected that chat_completion is not supported for currently.

        if prov.langchain_con == "ChatOllama":

            return StreamingResponse(
                complete_chat_ollama(
                    prompt=payload.prompt,
                    url=prov.base_url,
                    model=payload.model,
                    stream=payload.stream,
                    temperature=payload.parameters.temperature,
                    top_k=payload.parameters.top_k,
                    top_p=payload.parameters.top_p
                )
            )

        else:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail=f"Chat Completion not yet implemented for Provider '{prov.name}'"
            )

    except (ConnectTimeout, ConnectError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Provider"
        )