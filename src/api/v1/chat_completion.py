from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from httpx import ConnectTimeout, ConnectError
from sqlalchemy.orm import Session

from core.config import config
from core.logging import get_logger
from database.providers import get_all_provider_configurations, ProviderConfiguration
from database.session import get_db_session
from auth.dep_verify_user import depends_verify_user, VerifiedUser
from iom.chat_completion import PayloadChatCompletion
from providers.chat_completion import complete_chat

router = APIRouter()

log = get_logger()


@router.post(
    "/chat_completion",
    tags=["Chat Completion"],
    response_class=StreamingResponse
)
async def post_chat_completion(
    payload: PayloadChatCompletion,
    user: VerifiedUser = Depends(depends_verify_user),
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

        # TODO: Not sure what happens if we run into an unexpected/unsupported Provider/langchain_con...
        # TODO: Check how/what error is raised.

        return StreamingResponse(
            complete_chat(
                langchain_con=prov.langchain_con,
                encrypted_api_key=prov.encrypted_api_key,
                prompt=payload.prompt,
                base_url=prov.base_url,
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