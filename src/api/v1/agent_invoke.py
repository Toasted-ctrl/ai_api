import json
import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from httpx import ConnectTimeout, ConnectError
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from sqlalchemy.orm import Session

from auth.dep_verify_user import depends_verify_user, VerifiedUser
from core.config import config
from core.logging import get_logger
from core.model_types import model_config
from database.message_threads import verify_or_get_thread_id
from database.providers import ProviderConfiguration, get_provider_config
from database.session import get_db_session
from iom.agent import PayloadAgent, ResponseAgentRun
from providers.agent import build_agent_model, stream_agent, run_agent


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
    "/agent",
    tags=["Agent Invocation"],
    response_model=ResponseAgentRun,
    description=(
        "Invokes a non-streaming response from an agent (by agent_id), or a "
        "response from a model if an agent_id is not provided."
    )
)
async def agent_response(
    payload: PayloadAgent,
    user: VerifiedUser = Depends(depends_verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseAgentRun:
    try:
        # TODO: Implement custom agent calling by utilizing agent_id.
        if payload.agent_id:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Calling agents by agent_id is not implemented yet"
            )
        
        if payload.provider_settings.model not in model_config.CHAT_COMPLETION_MODELS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model not supported by Provider"
            )
        
        prov: ProviderConfiguration = get_provider_config(
            session=session,
            provider_name=payload.provider_settings.name,
            user_id=user.id
        )

        thread_id: uuid.UUID = verify_or_get_thread_id(
            session=session,
            user_id=user.id,
            thread_id=payload.thread_id
        )

        async with AsyncPostgresSaver.from_conn_string(
            conn_string=config.PG_CHECKPOINTER_URL
        ) as checkpointer:
            agent = build_agent_model(
                langchain_con=prov.langchain_con,
                model=payload.provider_settings.model,
                base_url=prov.base_url,
                temperature=payload.parameters.temperature,
                top_k=payload.parameters.top_k,
                top_p=payload.parameters.top_p,
                encrypted_api_key=prov.encrypted_api_key,
                tools=[],
                system_prompt=None,
                checkpointer=checkpointer,
            )

            result = await run_agent(
                agent=agent,
                prompt=payload.prompt,
                thread_id=thread_id,
                user_id=user.id
            )

        return {
            "thread_id": thread_id,
            "messages": [_serialize_event(m) for m in result['messages']]
        }


    except (ConnectTimeout, ConnectError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Provider"
        )


@router.post(
    "/agent/stream",
    tags=["Agent Invocation"],
    response_class=StreamingResponse,
    description=(
        "Invokes a streaming response from an agent (by agent_id), or a "
        "streaming response from a model if an agent_id is not provided."
    )
)
async def agent_response_stream(
    payload: PayloadAgent,
    user: VerifiedUser = Depends(depends_verify_user),
    session: Session = Depends(get_db_session)
) -> StreamingResponse:
    try:
        # TODO: Implement custom agent calling by utilizing agent_id.
        if payload.agent_id:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Calling agents by agent_id is not implemented yet"
            )

        if payload.provider_settings.model not in model_config.CHAT_COMPLETION_MODELS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Model not supported by Provider"
            )

        prov: ProviderConfiguration = get_provider_config(
            session=session,
            provider_name=payload.provider_settings.name,
            user_id=user.id
        )

        thread_id: uuid.UUID = verify_or_get_thread_id(
            session=session,
            user_id=user.id,
            thread_id=payload.thread_id
        )

        async def event_stream(thread_id: uuid.UUID):
            async with AsyncPostgresSaver.from_conn_string(
                conn_string=config.PG_CHECKPOINTER_URL
            ) as checkpointer:
                
                agent = build_agent_model(
                    langchain_con=prov.langchain_con,
                    model=payload.provider_settings.model,
                    base_url=prov.base_url,
                    temperature=payload.parameters.temperature,
                    top_k=payload.parameters.top_k,
                    top_p=payload.parameters.top_p,
                    encrypted_api_key=prov.encrypted_api_key,
                    tools=[],
                    system_prompt=None,
                    checkpointer=checkpointer,
                )

                async for event in stream_agent(
                    agent=agent,
                    prompt=payload.prompt,
                    thread_id=thread_id,
                    user_id=user.id
                ):
                    yield f"data: {json.dumps(_serialize_event(event=event))}\n\n"

        return StreamingResponse(
            event_stream(thread_id=thread_id),
            media_type="text/event-stream",
            headers={"X-Thread-ID": str(thread_id)}
        )

    except (ConnectTimeout, ConnectError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Provider"
        )