import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, Depends
from fastapi_limiter import FastAPILimiter
from starlette.middleware.cors import CORSMiddleware

from src.api.endpoints import auth_router, orders_router
from src.core.constants.api import ApiConstants
from src.infrastructure.message_broker.connection import rabbit_connection
from src.infrastructure.message_broker.consumer import run_consumer
from src.infrastructure.redis.order import redis_cache

from fastapi_limiter.depends import RateLimiter


@asynccontextmanager
async def lifespan(_: FastAPI):
    await rabbit_connection.run_initialize()
    asyncio.create_task(run_consumer())
    await FastAPILimiter.init(redis_cache.client)
    yield
    await rabbit_connection.disconnect()
    await FastAPILimiter.close()


app = FastAPI(
    lifespan=lifespan,
    dependencies=[
        Depends(RateLimiter(times=ApiConstants.request_per_second_limit, seconds=1))
    ],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ApiConstants.allowed_origins,
    allow_credentials=True,
    allow_methods=ApiConstants.allow_methods,
    allow_headers=ApiConstants.allow_headers,
)

base_router = APIRouter(prefix=ApiConstants.api_prefix)
base_router.include_router(auth_router, tags=["auth"])
base_router.include_router(orders_router, tags=["orders"])
app.include_router(base_router)
