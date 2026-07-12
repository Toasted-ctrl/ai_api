from fastapi import APIRouter

from io_models.root import ResponseRoot
from core.config import config

router = APIRouter()

@router.get("/", response_model=ResponseRoot, tags=["Root"])
def get_root():
    return {
        "detail": "Success",
        "application_name": config.app_name,
        "version": config.app_version,
        "contact": {
            "maintainer": config.app_maintainer
        }
    }