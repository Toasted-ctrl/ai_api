from httpx import ConnectError, ConnectTimeout
from sqlalchemy.orm import Session
from warnings import deprecated
import uuid

from core.logging import get_logger
from database.providers import get_all_provider_configurations
from providers.anthropic.models import get_models as get_models_anthropic
from providers.ollama.models import get_models as get_models_ollama
from providers.openai.models import get_models as get_models_openai

log = get_logger()


async def get_all_models(
    session: Session,
    user_id: uuid.UUID
) -> dict:
    """Returns a dictionary of all LLM providers, separated by provider.
    Per provider, all models are listed by area of expertise
    (e.g., chat_completion, translation, vector_embedding)."""

    # TODO: Write tests

    p_reg = get_all_provider_configurations(
        session=session,
        user_id=user_id
    )

    all_m = {}

    for p in p_reg:

        if p.requires_api_key and not p.api_key_configured:
            log.debug(f"Provider '{p.name}' not configured for User '{user_id}'...")
            continue

        try:

            if p.langchain_con == "ChatOllama":
                mds = await get_models_ollama(
                    base_url=p.base_url
                )

            # Anthropic based connectors
            elif p.langchain_con == "ChatAnthropic":
                mds = await get_models_anthropic(
                    encrypted_api_key=p.encrypted_api_key
                )

            # OpenAI based connectors
            elif p.langchain_con == "ChatOpenAI":
                mds = await get_models_openai(
                    encrypted_api_key=p.encrypted_api_key,
                    base_url=p.base_url
                )

            else:
                continue

            all_m[p.name] = mds

        except (ConnectTimeout, ConnectError):
            continue

    return all_m


@deprecated("This function is deprecated, please replace.")
def find_provider(data: dict, model_name):

    """Locates the provider that is currently hosting the model."""

    for provider in data.keys():
        provider_model_types = data.get(provider).keys()
        for model_type in provider_model_types:
            models = data.get(provider).get(model_type)
            if model_name in models:
                return provider
    return None