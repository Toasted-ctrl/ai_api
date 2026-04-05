import requests

def is_ollama_server_online(base_url) -> bool:

    """Checking if the Ollama server is online at the specified address."""

    response = requests.get(url=base_url)
    if not response.status_code == 200:
        return False
    return True