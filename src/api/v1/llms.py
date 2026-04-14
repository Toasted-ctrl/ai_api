from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from model_servers.ollama_1.llama31 import llm_stream

router = APIRouter()
tags = ["LLMs"]

@router.get(
    "/llms/stream",
    tags=tags
)
def get_llm_stream():
    return StreamingResponse(llm_stream(), media_type="text/plain")