from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from api.routers.trade import router
from config import REDIS_HOST, REDIS_PORT

def url_key_builder(func, *args, **kwargs):
    request = kwargs["request"]
    return str(request.url)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis_client = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache", key_builder=url_key_builder)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api")
