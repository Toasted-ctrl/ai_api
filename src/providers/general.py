from core.config import config
from providers.ollama.general import get_all_models_ollama

def _get_all_models() -> dict:

    """Returns a dictionary of all LLM providers, separated by provider.
    Per provider, all models are listed by area of expertise (e.g., chat_completion, translation, vector_embedding)."""

    all_providers = {}

    for provider in config.LOCAL_SERVER_CONFIGURATION.keys():
        all_providers[provider] = get_all_models_ollama(host_url=config.LOCAL_SERVER_CONFIGURATION[provider]['base_url'])

    return all_providers