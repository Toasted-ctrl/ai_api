from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from core.config import config
from models.m_llms import PayloadLLM
from model_servers.ollama.llms import llm_stream_ollama

router = APIRouter()
tags = ["LLMs"]

# TODO: Build test for the below endpoint

@router.post(
    "/llms/stream",
    tags=tags
)
def get_llm_stream(payload: PayloadLLM):
    if payload.model_name not in config.supported_models(type="llms"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Model not supported"
        )
    return StreamingResponse(
        llm_stream_ollama(
            query=payload.query,
            url=config.OLLAMA_BASE_URL,
            model=payload.model_name),
        media_type="text/plain")