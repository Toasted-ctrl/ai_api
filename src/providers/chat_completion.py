from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from typing import AsyncGenerator

from core.logging import get_logger
from providers.dataclasses import LangChainCon
from security.encryption import decrypt

log = get_logger()

# TODO: Build tests


def _build_llm(
    langchain_con: LangChainCon,
    model: str,
    base_url: str,
    temperature: float | None,
    top_k: int | None,
    top_p: float | None,
    encrypted_api_key: str | None,
) -> BaseChatModel:
    """Construct the correct LangChain chat model for the given provider."""

    common_kwargs = {
        "model": model,
        "base_url": base_url,
        "temperature": temperature,
        "top_p": top_p,
    }

    match langchain_con:
        case "ChatAnthropic":
            if encrypted_api_key is None:
                raise ValueError("encrypted_api_key is required for Anthropic")
            log.debug("Constructing Chat Model: ChatAnthropic")
            return ChatAnthropic(
                api_key=decrypt(encrypted_api_key),
                top_k=top_k,
                **common_kwargs,
            )

        case "ChatOpenAI":
            if encrypted_api_key is None:
                raise ValueError("encrypted_api_key is required for OpenAI")
            log.debug("Constructing Chat Model: ChatOpenAI")
            return ChatOpenAI(
                api_key=decrypt(encrypted_api_key),
                **common_kwargs,
            )

        case "ChatOllama":
            # Ollama is local — no API key needed
            log.debug("Constructing Chat Model: ChatOllama")
            return ChatOllama(
                top_k=top_k,
                **common_kwargs
            )

        case _:
            log.warning(f"Unsupported LangChain Chat Model: '{langchain_con}' ...")
            raise ValueError(f"Unsupported provider: {langchain_con}")


async def complete_chat(
    langchain_con: LangChainCon,
    model: str,
    prompt: str,
    base_url: str,
    stream: bool,
    encrypted_api_key: str | None = None,
    temperature: float | None = None,
    top_k: int | None = None,
    top_p: float | None = None,
) -> AsyncGenerator[str, None]:
    """Async generator that yields content chunks from any supported Provider."""

    llm = _build_llm(
        langchain_con=langchain_con,
        model=model,
        base_url=base_url,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        encrypted_api_key=encrypted_api_key,
    )

    log.debug("Chat Model constructed, returning/streaming Chat Completion content ...")

    if stream:
        async for chunk in llm.astream(prompt):
            if chunk.content:
                yield chunk.content

    else:
        response = await llm.ainvoke(prompt)
        if response.content:
            yield response.content