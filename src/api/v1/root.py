from fastapi import APIRouter

from models.m_root import ReturnRoot
from core.config import config

router = APIRouter()

@router.get("/", response_model=ReturnRoot, tags=["Root"])
def get_root():
    
    return {
        "detail": "Success",
        "application_name": config.app_name,
        "version": config.app_version,
        "contact": {
            "maintainer": config.app_maintainer
        }
    }