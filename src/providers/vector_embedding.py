from enum import Enum
from langchain_ollama import OllamaEmbeddings

from core.config import config
from core.logging import get_logger

log = get_logger()


class LangChainCon(str, Enum):
    ANTHROPIC = "ChatAnthropic"
    OLLAMA = "ChatOllama"
    OPENAI = "ChatOpenAI"


def _build_embedding_model(
    langchain_con: LangChainCon,
    model: str,
    base_url: str,
    encrypted_api_key: str | None = None
):
    """Embedding model factory."""

    # TODO: Add dimensions as well, in case the model supports variable dimensions.

    common_kwargs = {
        "model": model,
        "base_url": base_url,
    }

    # For now only one case for testing purposes, add more Provider options later on.

    match langchain_con:
        case LangChainCon.OLLAMA:
            log.debug(f"Requesting Ollama embedding model '{model}' ...")
            return OllamaEmbeddings(**common_kwargs)

        case _:
            raise NotImplementedError(f"Embedding not supported for '{langchain_con}' ...")


async def get_embedding(
    langchain_con: LangChainCon,
    model: str,
    prompt: str,
    base_url: str,
    encrypted_api_key: str | None = None
) -> list[float]:
    """Retrieve embedding from indicated Provider with specified Embedding model."""

    # TODO: Some Providers will probably not have any embedding models.
    # Figure out some way to block if an embedding model is requested from a Provider
    # that does not support it.

    if not model in config.VECTOR_EMBEDDING_MODELS:
        raise ValueError(f"'{model}' is not recognized as embedding model ...")

    embedding = _build_embedding_model(
        langchain_con=langchain_con,
        model=model,
        base_url=base_url,
        encrypted_api_key=encrypted_api_key
    )

    log.debug("Embedding Model constructed, generating embedding ...")

    result = await embedding.aembed_query(prompt)

    log.debug("Embedding complete, returning ...")

    return result