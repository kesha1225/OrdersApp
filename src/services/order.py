from typing import Sequence
from uuid import UUID

from fntypes import Ok, Error

from src.common.enums.error import RedisError, BaseErrorEnum
from src.common.fn import is_ok, is_err
from src.infrastructure.redis.order import redis_cache
from src.schemas.mappers.order import map_order_from_db
from src.schemas.order import OrderCreate, OrderStatusUpdate
from src.db.models import OrderDB
from src.repository.abstract.order import AbstractOrderRepository

from src.common.types_ import OrderDbResult, UpdateOrderDbResult, OrderSchemaResult


class OrderService:
    def __init__(self, user_repository: AbstractOrderRepository):
        self.order_repository = user_repository

    async def create(self, order_create: OrderCreate, user_id: UUID) -> OrderDbResult:
        return await self.order_repository.create(
            order_create=order_create, user_id=user_id
        )

    async def _get_by_id(self, order_id: UUID) -> OrderDbResult:
        return await self.order_repository.get_by_id(order_id=order_id)

    async def get_by_id(self, order_id: UUID) -> OrderSchemaResult:
        # fntypes waiting lazy
        # return (await redis_cache.get_order(order_id)).unwrap_or(
        #     await self.order_repository.get_by_id(order_id=order_id)
        # )

        cache_result = await redis_cache.get_order(order_id)

        if is_ok(cache_result):
            return cache_result

        current_order_result = await self._get_by_id(order_id=order_id)

        # is_err exists but pycharm moment
        if isinstance(current_order_result, Error):
            return current_order_result

        mapped_order = map_order_from_db(current_order_result.unwrap())

        await redis_cache.set_order(order=mapped_order)
        return Ok(mapped_order)

    async def update_status(
        self, order_id: UUID, order_update: OrderStatusUpdate
    ) -> UpdateOrderDbResult:
        return await self.order_repository.update_status(
            order_id=order_id, order_update=order_update
        )

    async def get_orders_by_user_id(self, user_id: UUID) -> Sequence[OrderDB]:
        return await self.order_repository.get_orders_by_user_id(user_id=user_id)
