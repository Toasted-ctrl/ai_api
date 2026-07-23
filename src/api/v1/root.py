from fastapi import APIRouter

from io_models.root import ResponseRoot
from core.config import config

router = APIRouter()

@router.get("/", response_model=ResponseRoot, tags=["Root"])
def get_root():
    return {
        "application_name": config.APP_NAME,
        "version": config.APP_VERSION,
        "contact": {
            "maintainer": config.APP_MAINTAINER
        }
    }