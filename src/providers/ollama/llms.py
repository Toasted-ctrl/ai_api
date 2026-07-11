import requests
from langchain_ollama import ChatOllama

from core.config import config

def ollama_llm_response(
    prompt: str,
    url: str,
    model: str,
    stream: bool = True,
    temperature: float | None = None,
    top_k: int | None = None,
    top_p: float | None = None
):
    
    """Returns a response from an LLM hosted on the Ollama server."""

    llm = ChatOllama(
        model=model,
        base_url=url,
        disable_streaming=True if stream == False else False,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p
    )

    for chunk in llm.stream(prompt):
        yield chunk.content


def ollama_get_llms(host_url) -> list[str]:

    """Returns a list of currently available models on the Ollama server.
    Translation and vector embedding models are excluded."""

    url = f"{host_url}/api/tags"
    response = requests.get(url=url)
    response.raise_for_status()
    models = response.json()

    ex_translation_models = [
        "translategemma:latest"
    ]

    ex_vector_embedding_models = [
        "mxbai-embed-large:latest"
    ]

    ex_models = list(set(ex_translation_models + ex_vector_embedding_models))

    return [model['name'] for model in models['models'] if model['name'] not in ex_models]