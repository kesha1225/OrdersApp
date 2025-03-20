import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import Field

from src.schemas.base import BaseSchema
from src.common.enums.order import OrderStatus
from src.common.types_ import OrderItems


class OrderCreate(BaseSchema):
    items: OrderItems
    total_price: Decimal = Field(..., gt=0)


class OrderStatusUpdate(BaseSchema):
    status: OrderStatus


class OrderBaseResponse(BaseSchema):
    id: UUID


class OrderDataSchema(OrderBaseResponse, OrderCreate):
    user_id: UUID
    status: OrderStatus
    created_at: datetime.datetime


class UserOrdersGetResponse(BaseSchema):
    orders: list[OrderDataSchema]
