from anthropic import AsyncAnthropic

from core.logging import get_logger

log = get_logger()


async def get_models(
    api_key: str
) -> dict[str: list[str]]:

    """Function that will return all available Anthropic models."""

    log.debug(f"Fetching Anthropic models with key '{api_key[:10]}'...")

    async with AsyncAnthropic(api_key=api_key) as client:

        models = await client.models.list()

        return {
            "chat_completion": [model.display_name for model in models.data],
            "translation": [],
            "vector_embedding": []
        }