from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import uvicorn

from api.v1 import chat_completion, jwt, root, servers, models, status, translation
from core.config import config
from core.logging import get_logger
from setup.create_frontend_client import create_frontend_client
from setup.create_tables import create_tables

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

app.include_router(
    router=jwt.router,
    prefix=v1_prefix
)

app.include_router(
    router=root.router,
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

if __name__ == "__main__":

    if config.CREATE_TABLES:
        create_tables()

    if config.FRONTEND_APP_CREATE_KEY:
        create_frontend_client(
            client=config.FRONTEND_APP_CLIENT,
            key_type=config.FRONTEND_APP_KEY_TYPE,
            owner_email=config.FRONTEND_APP_OWNER_EMAIL,
            require_external_id=config.FRONTEND_APP_REQUIRE_EXTERNAL_ID,
            require_jwt=config.FRONTEND_APP_REQUIRE_JWT,
            api_key=config.FRONTEND_APP_API_KEY,
            hmac_secret=config.FRONTEND_APP_HMAC
        )

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000
    )