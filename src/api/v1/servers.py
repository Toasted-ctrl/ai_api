from fastapi import APIRouter, HTTPException, status

from core.config import config
from io_models.servers import ResponseLocalServers, ResponseWakeServer
from servers.boot_server import wake_server
from servers.status import is_llm_available, is_server_online

router = APIRouter()

@router.get(
    "/servers/on_prem",
    tags=["Servers (On Prem)"],
    response_model=ResponseLocalServers
)
def get_local_servers():
    servers = []
    for server_name in config.LOCAL_SERVER_CONFIGURATION.keys():
        server = {}
        server['server_name'] = server_name
        server['online'] = is_server_online(
            host=config.LOCAL_SERVER_CONFIGURATION[server_name]['hostname']
        )
        server['available'] = is_llm_available(
            url=config.LOCAL_SERVER_CONFIGURATION[server_name]['base_url']
        )
        servers.append(server)

    return {
        "on_prem": servers
    }


@router.get(
    "/servers/on_prem/wake/{server_name}",
    tags=["Servers (On Prem)"],
    response_model=ResponseWakeServer
)
def wake_local_server(server_name: str):
    try:
        servers: dict = config.LOCAL_SERVER_CONFIGURATION
        if server_name not in servers.keys():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Server non-existant: {server_name}"
            )
        
        server: dict = servers.get(server_name)
        wake_server(mac_address=server.get('mac_address'))
        return {
            "detail": f"Magic packet sent to '{server_name}'. Please verify its status."
        }
    
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"MAC Address not configured for server: {server_name}"
        )