import requests
import socket

def is_server_online(host: str, port: int = 11434, timeout: float = 2.0) -> bool:
    
    """Returns True if the returns a response. Requires pinging IP address or hostname."""

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def is_llm_available(url) -> bool:

    """Returns True if the LLM service (e.g., Ollama) is available."""

    try:
        response = requests.get(url=url)
        if not response.status_code == 200:
            return False
        return True
    except Exception:
        return False