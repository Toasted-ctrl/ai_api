from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import uvicorn

from api.v1 import chat_completion, root, servers, models, status, translation
from core.config import config
from core.logging import get_logger

log = get_logger()

v1_prefix = "/api/v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        f"redis://{config.REDIS_USER}:{config.REDIS_PASSWORD}@{config.REDIS_HOSTNAME}:{config.REDIS_PORT}/0",
    )
    FastAPICache.init(RedisBackend(redis=redis), prefix=config.REDIS_PREFIX)
    log.info("Cache initialized!")
    yield
    await redis.close()

app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    lifespan=lifespan
)

app.include_router(root.router, prefix=v1_prefix)
app.include_router(servers.router, prefix=v1_prefix)
app.include_router(models.router, prefix=v1_prefix)
app.include_router(status.router, prefix=v1_prefix)
app.include_router(translation.router, prefix=v1_prefix)
app.include_router(chat_completion.router, prefix=v1_prefix)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000
    )