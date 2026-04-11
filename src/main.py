from fastapi import FastAPI

from api.v1 import root, servers, translate, models
from core.config import config

v1_prefix = "/api/v1"

app = FastAPI(
    title=config.app_name,
    version=config.app_version
)

app.include_router(root.router, prefix=v1_prefix)
app.include_router(translate.router, prefix=v1_prefix)
app.include_router(servers.router, prefix=v1_prefix)
app.include_router(models.router, prefix=v1_prefix)