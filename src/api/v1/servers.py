import requests

from fastapi import APIRouter, HTTPException, status

from core.config import config
from models.m_servers import ReturnWakeServer, ReturnServerStatus, ReturnServers
from servers.boot_server import boot_server
from servers.status import is_server_online

router = APIRouter()
tags = ["Servers"]

@router.get(
    "/servers",
    tags=tags,
    response_model=ReturnServers
)
def list_servers():
    servers: dict = config.get_servers
    return {
        "detail": "Success",
        "servers": [key for key in servers.keys()]
    }

@router.get(
    "/servers/{server_name}/wake",
    tags=tags,
    response_model=ReturnWakeServer
)
def wake_server(server_name: str):
    try:
        servers: dict = config.get_servers
        if server_name not in servers.keys():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Server not found: {server_name}"
            )
        
        server: dict = servers.get(server_name)
        boot_server(mac_address=server.get('mac_address'))
        return {
            "detail": f"Sent magic packet to '{server_name}' server. Please verify the server is online."
        }
    
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"MAC Address not configured for server: {server_name}"
        )

@router.get(
    "/servers/{server_name}/status",
    tags=tags,
    response_model=ReturnServerStatus
)
def get_server_status(server_name: str):
    try:
        servers: dict = config.get_servers
        if server_name not in servers.keys():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Server not found: {server_name}"
            )
    
        server: dict = servers.get(server_name)
        server_status: bool = is_server_online(url=server.get('base_url'))
        return {
            "server_name": server_name,
            "status": "Online",
            "available": server_status 
        }

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Server offline: {server_name}"
        )
    
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Base URL not configured for server: {server_name}"
        )