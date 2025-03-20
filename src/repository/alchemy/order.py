from typing import Literal, Sequence
from uuid import UUID

from fntypes import Error, Ok
from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.order import OrderCreate, OrderStatusUpdate
from src.common.enums.error import OrderError
from src.common.fn import from_optional
from src.common.types_ import OrderDbResult, UpdateOrderDbResult
from src.db.models import OrderDB
from src.repository.abstract.order import AbstractOrderRepository


class AlchemyOrderRepository(AbstractOrderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, order_create: OrderCreate, user_id: UUID) -> OrderDbResult:
        result = await self.session.execute(
            insert(OrderDB)
            .values(
                user_id=user_id,
                items=order_create.items,
                total_price=order_create.total_price,
            )
            .returning(OrderDB)
        )

        await self.session.commit()
        order = result.scalar_one_or_none()

        return from_optional(order).cast(error=OrderError.cant_create)

    async def get_by_id(self, order_id: UUID) -> OrderDbResult:
        result = await self.session.execute(
            select(OrderDB).where(OrderDB.id == order_id)
        )
        order = result.scalar_one_or_none()

        return from_optional(order).cast(error=OrderError.not_found)

    async def update_status(
        self, order_update: OrderStatusUpdate, order_id: UUID
    ) -> UpdateOrderDbResult:
        try:
            await self.session.execute(
                update(OrderDB)
                .where(OrderDB.id == order_id)
                .values(
                    status=order_update.status,
                )
            )
        except NoResultFound:
            return Error(OrderError.not_found)

        # 0_o
        await self.session.commit()
        return Ok[Literal[True]](True)

    async def get_orders_by_user_id(self, user_id: UUID) -> Sequence[OrderDB]:
        result = await self.session.execute(
            select(OrderDB).where(OrderDB.user_id == user_id)
        )
        return result.scalars().all()
