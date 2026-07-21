from typing import Optional

from core.config import config

def get_application(api_key: str) -> Optional[str]:

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