from warnings import deprecated
import httpx

from core.config import config

@deprecated("Replaced with 'get_models' from the providers.ollama.models module.")
async def get_all_models_ollama(host_url) -> list[str]:

    # TODO: Rework this function to use Ollama's AsyncClient instead.

    """Returns a dictionary of all available models on the Ollama server.
    Subdivided by expertise (e.g., chat_completion, translation, vector_embedding)."""

    url = f"{host_url}/api/tags"

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url)
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