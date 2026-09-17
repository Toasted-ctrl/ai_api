from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from httpx import ConnectTimeout, ConnectError
from sqlalchemy.orm import Session

from core.logging import get_logger
from core.model_types import model_config
from database.providers import ProviderConfiguration, get_provider_config
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

        if payload.model not in model_config.CHAT_COMPLETION_MODELS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model not supported by Provider"
            )

        prov: ProviderConfiguration = get_provider_config(
            session=session,
            provider_name=payload.provider,
            user_id=user.id
        )

        return StreamingResponse(
            complete_chat(
                langchain_con=prov.langchain_con,
                encrypted_api_key=prov.encrypted_api_key,
                user_id=user.id,
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