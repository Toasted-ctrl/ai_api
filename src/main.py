from fastapi import FastAPI
import uvicorn

from api.v1 import root, servers, models, status, translation, llms
from core.config import config

v1_prefix = "/api/v1"

app = FastAPI(
    title=config.app_name,
    version=config.app_version
)

app.include_router(root.router, prefix=v1_prefix)
app.include_router(servers.router, prefix=v1_prefix)
app.include_router(models.router, prefix=v1_prefix)
app.include_router(status.router, prefix=v1_prefix)
app.include_router(translation.router, prefix=v1_prefix)
app.include_router(llms.router, prefix=v1_prefix)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000)