from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fntypes import Ok, Error
from starlette import status

from src.api.dependencies import (
    get_authenticated_user_di,
    get_order_repository,
    get_order_service,
)
from src.infrastructure.redis.order import redis_cache
from src.schemas.mappers.order import map_orders_from_db
from src.schemas.order import (
    OrderCreate,
    OrderBaseResponse,
    OrderStatusUpdate,
    OrderDataSchema,
    UserOrdersGetResponse,
)
from src.core.constants.api import ApiConstants
from src.db.models import UserDB
from src.services.order import OrderService
from src.services.order_processing import post_create_order_actions

router = APIRouter(prefix=ApiConstants.orders_prefix)


@router.post(ApiConstants.create_order_prefix, response_model=OrderBaseResponse)
async def create_order(
    order_data: OrderCreate,
    user: Annotated[UserDB, Depends(get_authenticated_user_di)],
    order_service: Annotated[OrderService, Depends(get_order_repository)],
):
    match await order_service.create(user_id=user.id, order_create=order_data):
        case Ok(order):
            await post_create_order_actions(new_order=order)
            return OrderBaseResponse(id=order.id)
        case Error(error):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


@router.post(ApiConstants.order_id_prefix, response_model=OrderDataSchema)
async def get_order(
    order_id: UUID,
    order_service: Annotated[OrderService, Depends(get_order_service)],
):
    match await order_service.get_by_id(order_id=order_id):
        case Ok(order):
            return order
        case Error(error):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


@router.patch(ApiConstants.order_id_prefix, status_code=status.HTTP_204_NO_CONTENT)
async def update_order_status(
    order_id: UUID,
    order_update_data: OrderStatusUpdate,
    order_service: Annotated[OrderService, Depends(get_order_service)],
):
    match await order_service.update_status(
        order_id=order_id, order_update=order_update_data
    ):
        case Ok(_):
            await redis_cache.update_order_status(
                new_status=order_update_data.status, order_id=order_id
            )
        case Error(error):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


@router.get(ApiConstants.user_orders_prefix, response_model=UserOrdersGetResponse)
async def get_user_orders(
    user_id: UUID,
    order_service: Annotated[OrderService, Depends(get_order_repository)],
):
    orders = await order_service.get_orders_by_user_id(user_id=user_id)
    return map_orders_from_db(orders)
