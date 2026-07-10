from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from core.config import config
from io_models.llms import PostLLM
from providers.ollama.llms import ollama_llm_response, ollama_get_llms

router = APIRouter()
tags = ["Models", "LLMs"]

# TODO: Build test for the below endpoint

@router.post(
    "/models/llms",
    tags=tags
)
def post_llm(payload: PostLLM):

    if payload.provider not in config.SUPPORTED_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Unsupported Provider: '{payload.provider}'"
        )
    
    if payload.model is None and payload.agent is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Model or Agent must not be None"
        )
    
    if payload.provider == "Ollama":

        if payload.model is None:
            raise HTTPException(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Model must not be None for Provider Ollama."
            )

        return StreamingResponse(
            ollama_llm_response(
                prompt=payload.prompt,
                stream=payload.stream,
                model=payload.model,
                url=config.OLLAMA_BASE_URL,
                top_k=payload.parameters.top_k,
                top_p=payload.parameters.top_p,
                temperature=payload.parameters.temperature
            ),
            media_type="text/plain"
        )
    
@router.get(
    "/models/llms",
    tags=tags
)
def get_llms():
    models_ollama = ollama_get_llms()
    return {
        "providers": {
            "Ollama": models_ollama
        }
    }