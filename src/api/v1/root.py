from fastapi import (
    APIRouter,
    Request,
    Response
)
from fastapi_cache.decorator import cache

from io_models.root import ResponseRoot
from core.cache import cache_key_builder
from core.config import config

router = APIRouter()

@router.get(
    "",
    response_model=ResponseRoot,
    tags=["Default"]
)
@cache(expire=300, key_builder=cache_key_builder)
def get_root(
    request: Request,
    response: Response
) -> ResponseRoot:
    
    return {
        "application_name": config.APP_NAME,
        "version": config.APP_VERSION,
        "contact": {
            "maintainer": config.APP_MAINTAINER
        }
    }