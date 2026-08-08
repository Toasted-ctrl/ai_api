from openai import AsyncOpenAI

from core.logging import get_logger
from security.encryption import decrypt

log = get_logger()


async def get_models(
    encrypted_api_key: str,
    base_url: str
) -> dict[str, list[str]]:

    """Fetches and returns all models supported by the API Key.
    This method will work for both OpenAI as well as Melious endpoints."""

    log.debug(f"Fetching models for Provider URL '{base_url}' with API Key '{encrypted_api_key[:10]}'...")

    async with AsyncOpenAI(
        api_key=decrypt(content=encrypted_api_key),
        base_url=base_url
    ) as client:

        models = await client.models.list()

        # TODO: Likely build in some separation here, some models might be
        # Vector Embedding models or other types of models.
        
        return {
            "chat_completion": [model.id for model in models.data],
            "translation": [],
            "vector_embedding": []
        }