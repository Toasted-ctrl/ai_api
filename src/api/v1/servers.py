from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session

from core.logging import get_logger
from database.providers import get_providers_by_location
from database.session import get_db_session
from dependencies.d_v_user import dep_ver_usr, VerifiedUser
from io_models.servers import ResponseLocalServers
from servers.status import is_llm_available, is_server_online

log = get_logger()

router = APIRouter()


@router.get(
    "/servers",
    tags=["Servers (On Prem)"],
    response_model=ResponseLocalServers
)
def get_local_servers(
    user: VerifiedUser = Depends(dep_ver_usr),
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