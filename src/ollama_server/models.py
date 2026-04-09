import requests

from ollama_server.translategemma import get_languages as get_languages_translategemma

def get_models(base_url: str) -> list[dict]:

    """Retrieves a list of supported models on the Ollama server."""

    url = f"{base_url}/api/tags"
    response = requests.get(url=url)
    response.raise_for_status()
    return response.json()['models']
    
def get_translation_models(base_url: str) -> list[dict] | None:

    """Retrieves a list of translation models available on the Ollama server.
    Returns None if no translation models are found."""

    translation_models = [
        "translategemma:latest"
    ]

    models = get_models(base_url=base_url)
    if models == []:
        print("Cannot connect to Ollama server")
        return None

    t_models = []
    for m in models:
        t_model = {}
        if m.get('name') in translation_models:
            t_model['model_name'] = m.get('name')
            if m.get('name') == "translategemma:latest":
                t_model['language_codes'] = get_languages_translategemma()
        if not t_model == {}:
            t_models.append(t_model)

    if t_models == []:
        return None
    
    return t_models