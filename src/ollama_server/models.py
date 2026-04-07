import requests

from ollama_server.translategemma import get_languages as get_languages_translategemma

def get_ollama_models(base_url: str) -> list[dict] | None:

    """Retrieves a list of supported models on the Ollama server."""

    url = f"{base_url}/api/tags"
    try:
        response = requests.get(url=url)
        if not response.status_code == 200:
            return None
        if response.json()['models'] == []:
            return None
        return response.json()['models']
    except requests.exceptions.ConnectionError:
        print("Cannot connect to Ollama server")
        return None
    except requests.exceptions.RequestException as e:
        print(str(e))
        return None
    
def get_translation_models(base_url: str) -> list[dict] | None:

    """Retrieves a list of translation models available on the Ollama server."""

    supported_translation_models = [
        "translategemma:latest"
    ]

    models = get_ollama_models(base_url=base_url)
    if models == None:
        print("Cannot connect to Ollama server")
        return None

    online_models = []
    for m in models:
        online_model = {}
        if m.get('name') in supported_translation_models:
            online_model['model_name'] = m.get('name')
            if m.get('name') == "translategemma:latest":
                online_model['language_codes'] = get_languages_translategemma()
        if not online_model == {}:
            online_models.append(online_model)

    if online_models == []:
        return None
    
    return online_models