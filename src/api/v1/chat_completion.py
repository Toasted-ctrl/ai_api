from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse

from auth.hmac import verify_hmac_signature
from core.config import config
from core.logging import get_logger
from io_models.chat_completion import PayloadChatCompletion
from providers.ollama.chat_completion import complete_chat_ollama
from providers.ollama.general import is_ollama_model_supported

router = APIRouter()

log = get_logger()

@router.post(
    "/chat_completion",
    tags=["Chat Completion"],
    dependencies=[Depends(verify_hmac_signature)]
)
async def post_chat_completion(payload: PayloadChatCompletion):

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

        host = config.LOCAL_SERVER_CONFIGURATION["Ollama-1"]['base_url']

        await is_ollama_model_supported(model=payload.model, host=host)

        return StreamingResponse(
            complete_chat_ollama(
                prompt=payload.prompt,
                stream=payload.stream,
                model=payload.model,
                url=host,
                top_k=payload.parameters.top_k,
                top_p=payload.parameters.top_p,
                temperature=payload.parameters.temperature
            ),
            media_type="text/plain"
        )