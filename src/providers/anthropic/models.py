from anthropic import AsyncAnthropic

from core.logging import get_logger
from core.model_types import model_config
from security.encryption import decrypt


log = get_logger()


async def get_models(
    encrypted_api_key: str
) -> dict[str: list[str]]:
    """Function that will return all available Anthropic models."""

    log.debug(f"Fetching Anthropic models with key '{encrypted_api_key[:10]}'...")

    async with AsyncAnthropic(api_key=decrypt(content=encrypted_api_key)) as client:

        models = await client.models.list()

        return {
            "chat_completion": [model.id for model in models.data if model.id in model_config.CHAT_COMPLETION_MODELS],
            "translation": [model.id for model in models.data if model.id in model_config.TRANSLATION_MODELS],
            "vector_embedding": [model.id for model in models.data if model.id in model_config.VECTOR_EMBEDDING_MODELS]
        }