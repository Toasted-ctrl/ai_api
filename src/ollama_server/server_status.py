import requests

def is_ollama_server_online(base_url) -> bool:

    """Checking if the Ollama server is online at the specified address."""

    try:
        response = requests.get(url=base_url)
        if not response.status_code == 200:
            return False
        return True
    except requests.exceptions.ConnectionError:
        print("Cannot connect to Ollama server")
        return False
    except requests.exceptions.RequestException as e:
        print(str(e))
        return False