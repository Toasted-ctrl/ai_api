import platform
import requests
import subprocess

def is_server_online(host: str) -> bool:
    
    """Returns True if the returns a response. Requires pinging IP address or hostname."""

    # -n for Windows, -c for Unix
    param = "-n" if platform.system().lower() == "Windows" else "-c"
    result = subprocess.run(
        ["ping", param, "1", host]
    )

    # Return True if online
    return result.returncode == 0 


def is_llm_available(url) -> bool:

    """Returns True if the LLM service (e.g., Ollama) is available."""

    try:
        response = requests.get(url=url)
        if not response.status_code == 200:
            return False
        return True
    except Exception:
        return False