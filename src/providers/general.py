from httpx import ConnectError, ConnectTimeout
from sqlalchemy.orm import Session

from database.providers import get_providers_by_location
from providers.ollama.general import get_all_models_ollama

async def get_all_models(
    session: Session
) -> dict:

    # TODO: In the future, for external Providers, only return models that they have access to.
    # If no valid api key is set, the provider should not be shown.

    """Returns a dictionary of all LLM providers, separated by provider.
    Per provider, all models are listed by area of expertise (e.g., chat_completion, translation, vector_embedding)."""

    all_models_by_provider = {}

    internal_providers = get_providers_by_location(
        session=session,
        is_internal=True
    )

    for ip in internal_providers:
        try:
            models = await get_all_models_ollama(
                host_url=ip.base_url
            )
            all_models_by_provider[ip.name] = models
        except (ConnectTimeout, ConnectError):
            continue

    return all_models_by_provider


def find_provider(data: dict, model_name):

    """Locates the provider that is currently hosting the model."""

    for provider in data.keys():
        provider_model_types = data.get(provider).keys()
        for model_type in provider_model_types:
            models = data.get(provider).get(model_type)
            if model_name in models:
                return provider
    return None