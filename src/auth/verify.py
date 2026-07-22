from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional

from core.config import config

def get_client(api_key: str) -> Optional[str]:

    """Retrieves which client belongs to the API Key.
    Returns None if the API Key does not match any client."""

    for key, app in config.APPLICATIONS.items():
        if app.api_key == api_key:
            return key
    return None


def require_google_id(client: str) -> bool:

    """Indicated whether a client requires a Google ID (sub),
    to retrieve a JWT."""

    return config.APPLICATIONS[client].require_google_id


api_key_header = APIKeyHeader(name="X-API-Key")

async def get_client_from_key(api_key: str = Security(api_key_header)) -> str:

    # TODO: We'll probably want to host clients in a database later.

    if not api_key or get_client(api_key=api_key) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API Key"
        )

    return get_client(api_key=api_key)