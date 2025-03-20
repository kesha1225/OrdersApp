import abc
from typing import Sequence
from uuid import UUID

from src.schemas.order import OrderCreate, OrderStatusUpdate
from src.common.types_ import OrderDbResult, UpdateOrderDbResult
from src.db.models import OrderDB


class AbstractOrderRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, order_id: UUID) -> OrderDbResult: ...

    @abc.abstractmethod
    async def create(
        self, order_create: OrderCreate, user_id: UUID
    ) -> OrderDbResult: ...

    @abc.abstractmethod
    async def update_status(
        self, order_update: OrderStatusUpdate, order_id: UUID
    ) -> UpdateOrderDbResult: ...

    @abc.abstractmethod
    async def get_orders_by_user_id(self, user_id: UUID) -> Sequence[OrderDB]: ...
