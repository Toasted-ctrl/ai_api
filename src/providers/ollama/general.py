import requests

from core.config import config

def get_all_models_ollama(host_url) -> list[str]:

    """Returns a dictionary of all available models on the Ollama server.
    Subdivided by expertise (e.g., chat_completion, translation, vector_embedding)."""

    url = f"{host_url}/api/tags"
    response = requests.get(url=url)
    response.raise_for_status()
    output = response.json()
    models = [model['name'] for model in output['models']]

    all_models = {}

    all_models['chat_completion'] = [model for model in models if
                                      model not in config.TRANSLATION_MODELS and
                                      model not in config.VECTOR_EMBEDDING_MODELS]
    
    all_models['translation'] = [model for model in models if model in config.TRANSLATION_MODELS]

    all_models['vector_embedding'] = [model for model in models if model in config.VECTOR_EMBEDDING_MODELS]

    return all_models