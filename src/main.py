from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import uvicorn

from api.v1 import chat_completion, root, servers, models, status, translation, providers
from api.v1.login import google_login
from core.config import config
from core.logging import get_logger
from setup.create_tables import create_tables
from setup.preconfigurations import (
    create_preconfigured_clients,
    create_preconfigured_providers
)

log = get_logger()

v1_prefix = "/api/v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        f"redis://{config.REDIS_USER}:{config.REDIS_PASSWORD}@{config.REDIS_HOSTNAME}:{config.REDIS_PORT}/0",
    )
    FastAPICache.init(RedisBackend(redis=redis), prefix=config.REDIS_PREFIX)
    log.info("Redis cache initialized")
    yield
    await redis.close()

app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    lifespan=lifespan
)

if config.ENABLE_GOOGLE_LOGIN:
    log.debug("Starting with Google Login enabled...")
    app.include_router(
        router=google_login.router,
        prefix=v1_prefix
    )

app.include_router(
    router=root.router,
    prefix=v1_prefix
)

app.include_router(
    router=providers.router,
    prefix=v1_prefix
)

app.include_router(
    router=servers.router,
    prefix=v1_prefix
)

app.include_router(
    router=models.router,
    prefix=v1_prefix
)

app.include_router(
    router=status.router,
    prefix=v1_prefix
)

app.include_router(
    router=translation.router,
    prefix=v1_prefix
)

app.include_router(
    router=chat_completion.router,
    prefix=v1_prefix
)

@app.middleware("http")
async def secure_logging(request: Request, call_next):
    response = await call_next(request)

    path = request.url.path
    if "/auth/" in path or "/callback" in path:
        log.info(
            f"{request.client.host} - "
            f"\"{request.method} {path}\" "
            f"{response.status_code}"
        )
    else:
        log.info(
            f"{request.client.host} - "
            f"\"{request.method} {request.url}\" "
            f"{response.status_code}"
        )

    return response

if __name__ == "__main__":

    if config.CREATE_TABLES:
        create_tables()

    if config.CREATE_PRECONFIGURED_CLIENTS:
        try:
            create_preconfigured_clients()
        except ValueError as e:
            log.info(e)

    if config.CREATE_PRECONFIGURED_PROVIDERS:
        create_preconfigured_providers()

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
        access_log=False
    )