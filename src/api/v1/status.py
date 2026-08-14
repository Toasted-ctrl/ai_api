from fastapi import APIRouter

from iom.status import ResponseStatus

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