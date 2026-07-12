from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from core.config import config
from io_models.chat_completion import PayloadChatCompletion
from providers.ollama.chat_completion import complete_chat_ollama

router = APIRouter()

@router.post(
    "/chat_completion",
    tags=["Chat Completion"]
)
def post_chat_completion(payload: PayloadChatCompletion):

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
    
    if payload.provider == "Ollama-1":

        if payload.model is None:
            raise HTTPException(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Model must not be None for Provider Ollama."
            )

        return StreamingResponse(
            complete_chat_ollama(
                prompt=payload.prompt,
                stream=payload.stream,
                model=payload.model,
                url=config.LOCAL_SERVER_CONFIGURATION["Ollama-1"]['base_url'],
                top_k=payload.parameters.top_k,
                top_p=payload.parameters.top_p,
                temperature=payload.parameters.temperature
            ),
            media_type="text/plain"
        )