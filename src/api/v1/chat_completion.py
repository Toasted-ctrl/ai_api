from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from ollama import Client

from auth.hmac import verify_hmac_signature
from core.config import config
from io_models.chat_completion import PayloadChatCompletion
from providers.ollama.chat_completion import complete_chat_ollama

router = APIRouter()

@router.post(
    "/chat_completion",
    tags=["Chat Completion"],
    dependencies=[Depends(verify_hmac_signature)]
)
def post_chat_completion(payload: PayloadChatCompletion):

    # TODO: This whole path currently works, but we'll probably want to rework it. Messy.

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

        host_url = config.LOCAL_SERVER_CONFIGURATION["Ollama-1"]['base_url']

        client = Client(host=host_url)
        if payload.model not in client.list():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model '{payload.model}' not supported. Pull the model first on the '{payload.provider}' instance."
            )

        return StreamingResponse(
            complete_chat_ollama(
                prompt=payload.prompt,
                stream=payload.stream,
                model=payload.model,
                url=host_url,
                top_k=payload.parameters.top_k,
                top_p=payload.parameters.top_p,
                temperature=payload.parameters.temperature
            ),
            media_type="text/plain"
        )