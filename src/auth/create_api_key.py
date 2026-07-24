import secrets


def create_api_key() -> str:

    """Creates a new random API key"""

    return secrets.token_urlsafe(nbytes=64)