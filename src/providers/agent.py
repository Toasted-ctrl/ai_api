from langchain.agents import create_agent
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph.state import CompiledStateGraph
from typing import AsyncGenerator, Any, TypedDict, Literal
import uuid

from core.langfuse import langfuse_handler
from core.logging import get_logger
from providers.chat_completion import _build_llm
from providers.dataclasses import LangChainCon

log = get_logger()


def build_agent_model(
    langchain_con: LangChainCon,
    model: str,
    base_url: str,
    temperature: float | None,
    top_k: int | None,
    top_p: float | None,
    encrypted_api_key: str | None,
    tools: list,
    system_prompt: str | None = None,
    checkpointer: AsyncPostgresSaver | None = None,
) -> CompiledStateGraph:

    log.debug("Creating agent ...")

    model = _build_llm(
        langchain_con=langchain_con,
        model=model,
        base_url=base_url,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        encrypted_api_key=encrypted_api_key
    )

    log.debug("Built Model to add to agent ...")

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer
    )

    log.debug("Agent created, returning ...")

    return agent


class AgentEvent(TypedDict):
    type: Literal["message", "update", "error"]
    data: dict[str, Any]


def _extract_content(token: Any) -> str:
    if hasattr(token, "text") and token.text:
        return token.text
    content = getattr(token, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            b.get("text", "") for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


async def stream_agent(
    agent: CompiledStateGraph,
    prompt: str,
    thread_id: uuid.UUID
) -> AsyncGenerator[AgentEvent, None]:

    config = {
        "configurable": {
            "thread_id": str(thread_id)
        },
        "callbacks": [langfuse_handler],
        "metadata": {
            "langfuse_session_id": str(thread_id)
        }
    }
    
    yield {"type": "thread", "data": {"thread_id": str(thread_id)}}
    async for event in agent.astream(
        {"messages": [{"role": "user", "content": prompt}]},
        config=config,
        stream_mode=["messages", "updates"],
        version="v2",
    ):
        if event["type"] == "messages":
            token, metadata = event["data"]
            content = _extract_content(token)
            if content:
                yield {"type": "message", "data": {"content": content, "metadata": metadata}}

        elif event["type"] == "updates":
            yield {"type": "update", "data": event["data"]}