import anthropic

from core.logging import get_logger

log = get_logger()

def get_models(
    api_key: str
) -> dict[str: list[str]]:

    """Function that will return all available Anthropic models."""

    log.debug(f"Fetching Anthropic models with key '{api_key[:10]}'...")

    client = anthropic.Anthropic(api_key=api_key)
    models = client.models.list()

    return {
        "chat_completion": [model.display_name for model in models.data],
        "translation": [],
        "vector_embedding": []
    }