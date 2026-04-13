from fastapi import APIRouter

from models.m_status import ReturnStatus

router = APIRouter()
tags = ["Status"]

@router.get(
    "/status",
    tags=tags,
    response_model=ReturnStatus
)
def get_status():
    return {
        "status": "OK"
    }