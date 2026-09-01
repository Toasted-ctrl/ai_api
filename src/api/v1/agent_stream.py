from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from httpx import ConnectTimeout, ConnectError
from langchain_core.messages import BaseMessage
from sqlalchemy.orm import Session
import json
import uuid

from auth.dep_verify_user import depends_verify_user, VerifiedUser
from core.config import config
from core.logging import get_logger
from database.providers import get_all_provider_configurations, ProviderConfiguration
from database.session import get_db_session
from iom.agent_stream import PayloadAgentStream
from providers.agent import build_agent_model, stream_agent

router = APIRouter()

log = get_logger()


def _serialize_event(event):
    """Recursively convert LangChain messages to dicts."""
    if isinstance(event, BaseMessage):
        return event.model_dump()
    elif isinstance(event, dict):
        return {k: _serialize_event(v) for k, v in event.items()}
    elif isinstance(event, list):
        return [_serialize_event(item) for item in event]
    return event


@router.post(
    "/agent/stream",
    tags=["Agent"],
    response_class=StreamingResponse,
)
async def stream_agent_response(
    payload: PayloadAgentStream,
    user: VerifiedUser = Depends(depends_verify_user),
    session: Session = Depends(get_db_session)
) -> StreamingResponse:

    try:
        # TODO: Implement custom agent calling by utilizing thread_id.
        if payload.agent_id:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Calling agents by agent_id is not implemented yet"
            )

        if payload.model not in config.CHAT_COMPLETION_MODELS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model not supported by Provider"
            )

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

        if not payload.thread_id:
            thread_id = uuid.uuid4()
        else:
            thread_id = uuid.UUID(payload.thread_id)

        agent = build_agent_model(
            langchain_con=prov.langchain_con,
            model=payload.model,
            base_url=prov.base_url,
            temperature=payload.parameters.temperature,
            top_k=payload.parameters.top_k,
            top_p=payload.parameters.top_p,
            encrypted_api_key=prov.encrypted_api_key,
            tools=[],
            system_prompt=None
        )

        async def event_stream(thread_id: uuid.UUID):
            async for event in stream_agent(agent=agent, prompt=payload.prompt, thread_id=thread_id):
                yield f"data: {json.dumps(_serialize_event(event=event))}\n\n"

        return StreamingResponse(
            event_stream(thread_id=thread_id),
            media_type="text/event-stream",
            headers={
                "X-Thread-ID": str(thread_id)
            }
        )

    except (ConnectTimeout, ConnectError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Provider"
        )