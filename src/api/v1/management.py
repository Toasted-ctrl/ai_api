from fastapi import APIRouter, HTTPException, status

from core.config import config
from models.m_server_management import ReturnWakeServer
from server_management.boot_server import boot_server

router = APIRouter()
tags = ["Server Management"]

@router.get(
    "/management/wake_server/{server_name}",
    tags=tags,
    response_model=ReturnWakeServer)
def wake_server(server_name: str):

    # NOTE: Maybe we need to change this later and manage the list of servers elsewhere?

    if server_name not in ["ollama"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Server '{server_name}' does not exist")
    
    if server_name == 'ollama':
        boot_server(config.OLLAMA_MAC)

    return {
        "detail": f"Sent magic packet to '{server_name}' server. Please verify the server is online."
    }

# TODO: Create a new endpoint to fetch available models