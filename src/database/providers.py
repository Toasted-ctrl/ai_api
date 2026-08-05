from dataclasses import dataclass
from sqlalchemy.orm import Session

from core.logging import get_logger
from database.schemas.providers import ProvidersT

log = get_logger()


@dataclass(frozen=True)
class Provider:
    id: str
    name: str
    base_url: str
    internal: bool
    requires_api_key: bool
    langchain_con: str
    api_key_configured: bool | None = None
    mac_address: str | None = None


def get_or_create_provider(
    session: Session,
    id: str,
    name: str,
    langchain_con: str,
    base_url: str,
    internal: bool,
    requires_api_key: bool,
    host: str | None = None,
    mac_address: str | None = None
) -> Provider:

    """Creates a new or fetches existing Provider."""

    existing = (
        session.query(ProvidersT)
        .filter(
            ProvidersT.base_url == base_url
        )
        .first()
    )

    if existing:
        log.info(f"Provider '{name}' with url '{base_url}' already exists, fetching existing Provider...")
        return Provider(
            id=existing.id,
            name=existing.name,
            base_url=existing.base_url,
            internal=existing.internal,
            requires_api_key=existing.requires_api_key,
            langchain_con=existing.langchain_con
        )

    log.info("Creating new Provider...")

    new_provider = ProvidersT(
        id=id,
        name=name,
        langchain_con=langchain_con,
        base_url=base_url,
        internal=internal,
        requires_api_key=requires_api_key,
        host=host,
        mac_address=mac_address
    )

    session.add(new_provider)
    session.flush()

    log.info(f"New Provider created with url '{new_provider.base_url}', returning new Provider...")

    return Provider(
        id=new_provider.id,
        name=new_provider.name,
        base_url=new_provider.base_url,
        internal=new_provider.internal,
        requires_api_key=new_provider.requires_api_key,
        langchain_con=new_provider.langchain_con
    )


def get_provider(
    session: Session,
    provider_name: str
) -> Provider | None:

    """Fetches the details for ONE Provider."""

    provider = (
        session.query(ProvidersT)
        .filter(ProvidersT.name == provider_name)
        .one_or_none()
    )

    if not provider:
        log.debug(f"Provider '{provider_name}' could not be located...")
        return None

    return Provider(
        id=provider.id,
        name=provider.name,
        base_url=provider.base_url,
        internal=provider.internal,
        requires_api_key=provider.requires_api_key,
        langchain_con=provider.langchain_con,
        mac_address=provider.mac_address
    )


def get_all_providers_support_user(
    session: Session,
    user_provider_api_key_ids: list[str] | None = None
) -> list[Provider]:

    """Fetches a list of available configured AI providers,
    including whether API keys are configured for external providers."""

    if user_provider_api_key_ids is None:
        user_provider_api_key_ids = []

    providers = (
        session.query(
            ProvidersT.id,
            ProvidersT.base_url,
            ProvidersT.name,
            ProvidersT.langchain_con,
            ProvidersT.internal,
            ProvidersT.requires_api_key
        )
        .all()
    )

    return [
        Provider(
            id=p.id,
            base_url=p.base_url,
            name=p.name,
            langchain_con=p.langchain_con,
            internal=p.internal,
            requires_api_key=p.requires_api_key,
            api_key_configured=p.id in user_provider_api_key_ids
        )
    for p in providers
    ]


def get_providers_by_location(
    session: Session,
    is_internal: bool
) -> list[Provider]:

    """Returns a list of providers based on location (internal or external)."""

    providers = (
        session.query(
            ProvidersT.id,
            ProvidersT.base_url,
            ProvidersT.name,
            ProvidersT.internal,
            ProvidersT.requires_api_key,
            ProvidersT.langchain_con
        )
        .filter(ProvidersT.internal == is_internal)
        .all()
    )

    if not providers:
        return []

    return [
        Provider(
            id=p.id,
            base_url=p.base_url,
            name=p.name,
            langchain_con=p.langchain_con,
            internal=p.internal,
            requires_api_key=p.requires_api_key,
        )
    for p in providers
    ]