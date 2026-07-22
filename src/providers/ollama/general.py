from fastapi import HTTPException, status
from ollama import AsyncClient
import httpx

from core.config import config

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


async def is_ollama_model_supported(model: str, host: str) -> bool:

    """Confirms if a model is supported on the Ollama server.
    Raises a HTTPException if the model is not supported."""

    client = AsyncClient(host=host)
    response = await client.list()
    models = [m.model for m in response.models]
    if not model in models:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model '{model}' not supported. Pull the model on the Ollama server first."
        )

    return True