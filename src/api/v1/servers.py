from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends
)
from sqlalchemy.orm import Session

from auth.user import verify_user, VerifiedUser
from core.logging import get_logger
from database.providers import get_provider, Provider, get_providers_by_location
from database.session import get_db_session
from io_models.servers import ResponseLocalServers, ResponseWakeServer
from servers.wake import wake_server
from servers.status import is_llm_available, is_server_online

log = get_logger()

router = APIRouter()


@router.get(
    "/servers",
    tags=["Servers (On Prem)"],
    response_model=ResponseLocalServers
)
def get_local_servers(
    user: VerifiedUser = Depends(verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseLocalServers:

    providers = get_providers_by_location(
        session=session,
        is_internal=True
    )

    on_prem = []

    for provider in providers:
        provider_status = {}
        provider_status['server_name'] = provider.name
        provider_status['online'] = is_server_online(host=provider.mac_address) # TODO: Bugged, shows server as offline, but is online.
        provider_status['available'] = is_llm_available(url=provider.base_url)
        on_prem.append(provider_status)

    return {
        "on_prem_servers": on_prem
    }


@router.get(
    "/servers/wake/{provider_name}",
    tags=["Servers (On Prem)"],
    response_model=ResponseWakeServer
)
def wake_local_server(
    provider_name: str,
    user: VerifiedUser = Depends(verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseWakeServer:

    # TODO: Should only be accessible to Admins perhaps?
    
    provider: Provider = get_provider(
        session=session,
        provider_name=provider_name
    )

    # TODO: This is probably not the best way to check if the provider_name is internal.
    # Works but rewrite later.

    if provider.mac_address is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send magic packet to external Provider"
        )

    wake_server(mac_address=provider.mac_address)
    log.info(f"Sent magic packet to '{provider.mac_address}'...")

    return {
        "detail": f"Magic packet sent to {provider_name}. Please check if the server has come online."
    }