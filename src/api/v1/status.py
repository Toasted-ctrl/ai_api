from fastapi import APIRouter

from io_models.status import ResponseStatus

router = APIRouter()
tags = ["Status"]

@router.get(
    "/status",
    tags=tags,
    response_model=ResponseStatus
)
def get_status():
    return {
        "status": "OK"
    }