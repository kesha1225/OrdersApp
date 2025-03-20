from uuid import UUID

import redis.asyncio as redis

from fntypes import Ok, Error

from src.common.enums.error import RedisError
from src.common.enums.order import OrderStatus
from src.core.config.compilation import RedisConfig
from src.core.constants.redis import RedisConstants
from src.schemas.mappers.order import (
    map_order_schema_to_redis,
    map_order_schema_from_redis,
)
from src.schemas.order import OrderDataSchema

from src.common.types_ import OrderCacheGetResult


def get_order_key(order_id: UUID) -> str:
    return f"{RedisConstants.order_cache_prefix}:{order_id}"


class RedisCache:
    def __init__(self):
        self.client = redis.from_url(
            RedisConfig.redis_url.unicode_string(), decode_responses=True
        )

    async def get_order(self, order_id: UUID) -> OrderCacheGetResult:
        cached_order = await self.client.hgetall(get_order_key(order_id))  # pyright: ignore [reportGeneralTypeIssues]
        if not cached_order:
            return Error(RedisError.not_found)

        # можно и сериализацию кешить на мегахайлоаде
        return Ok(map_order_schema_from_redis(cached_order))

    async def set_order(self, order: OrderDataSchema) -> None:
        key = get_order_key(order.id)
        mapped = map_order_schema_to_redis(order=order)

        # Union[Awaitable[int], int] nice typing bros
        await self.client.hset(key, mapping=mapped)  # pyright: ignore [reportGeneralTypeIssues]
        await self.client.expire(key, RedisConstants.order_cache_seconds)

    async def update_order_status(
        self, order_id: UUID, new_status: OrderStatus
    ) -> None:
        await self.client.hset(get_order_key(order_id), "status", new_status)  # pyright: ignore


redis_cache = RedisCache()
