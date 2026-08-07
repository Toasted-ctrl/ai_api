from collections import namedtuple
from httpx import ConnectError, ConnectTimeout
from sqlalchemy.orm import Session
import uuid

from core.logging import get_logger
from database.providers import (
    get_providers_by_location,
    Provider,
    get_providers_by_id
)
from database.user_keys import get_user_active_keys
from providers.anthropic.models import get_models as get_models_anthropic
from providers.ollama.general import get_all_models_ollama
from providers.openai.models import get_models as get_models_openai

log = get_logger()


async def get_all_models(
    session: Session,
    user_id: uuid.UUID
) -> dict:

    # TODO: Write test.

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

    # Retrieve all active user keys.
    _keys = get_user_active_keys(
        session=session,
        user_id=user_id
    )

    if len(_keys) == 0:
        return all_models_by_provider

    ProviderKey = namedtuple(
        "ProviderKey", ["provider_id", "api_key"]
    )

    # Retrieveing all api keys and provider ids which the User has configured.
    # TODO: Maybe this is a bit too complicated for a simple check. Simplify somehow?
    keys = [ProviderKey(provider_id=k.provider_id, api_key=k.api_key) for k in _keys]

    providers = get_providers_by_id(
        session=session,
        ids=[p.provider_id for p in keys]
    )

    for p in providers:
        api_key = [k.api_key for k in keys if k.provider_id == p.id][0]
        base_url = p.base_url

        # Anthropic
        if p.name == "Anthropic":
            mds = get_models_anthropic(
                api_key=api_key
            )

        # Melious
        if p.name == "Melious":
            mds = get_models_openai(
                api_key=api_key,
                base_url=base_url
            )

        all_models_by_provider[p.name] = mds

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


def get_providers_configured_user(
    providers: list[Provider]
) -> list[Provider]:

    """Iterates through a list of Provider objects and returns only the Provider objects
    to which the user has access."""

    log.info("Verifying configured Providers...")

    return [
        p for p in providers
        if p.internal
        or (p.requires_api_key and p.api_key_configured)
    ]


# TODO: Build a function that checks if a user has access to a particular provider.
# Return the provider object.