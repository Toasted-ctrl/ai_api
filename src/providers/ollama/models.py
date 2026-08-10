from ollama import AsyncClient

from core.config import config


async def get_models(
    base_url: str
) -> dict[str, list[str]]:
    """Fetches and returns a dictionary of available models for the Ollama instance,
    subdivided by model 'Expertise'."""

    async with AsyncClient(host=base_url) as client:

        response = await client.list()

        mds = [model.model for model in response.models]

        # Chat Completion models
        ccm = [
            m for m in mds
            if m in config.CHAT_COMPLETION_MODELS
        ]

        # Vector Embedding models
        vem = [
            m for m in mds
            if m in config.VECTOR_EMBEDDING_MODELS
        ]

        # Translation models
        tm = [
            m for m in mds
            if m in config.TRANSLATION_MODELS
        ]

        return {
            "chat_completion": ccm,
            "translation": tm,
            "vector_embedding": vem
        }