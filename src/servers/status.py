import requests

def is_server_online(url) -> bool:

    """Checking if the Ollama server is online at the specified address."""

    response = requests.get(url=url)
    if not response.status_code == 200:
        return False
    return True