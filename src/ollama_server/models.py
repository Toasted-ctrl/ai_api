import requests

from ollama_server.translategemma import get_languages as get_languages_translategemma

def get_models(base_url: str) -> list[dict]:

    """Retrieves a list of supported models on the Ollama server.
    Returns empty list if no models were found."""

    url = f"{base_url}/api/tags"
    response = requests.get(url=url)
    response.raise_for_status()
    return response.json()['models']
    
def get_translators(models: list[dict]) -> list[dict]:

    """Retrieves a list of translation supported models on the Ollama server.
    Returns empty list if no translation models were found."""

    translation_models = [
        "translategemma:latest"
    ]

    t_models = []
    for m in models:
        t_model = {}
        if m.get('name') in translation_models:
            t_model['model_name'] = m.get('name')
            if m.get('name') == "translategemma:latest":
                t_model['language_codes'] = get_languages_translategemma()
        if not t_model == {}:
            t_models.append(t_model)

    return t_models