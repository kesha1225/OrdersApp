import json
import typing
from typing import Sequence

from src.schemas.order import OrderDataSchema, UserOrdersGetResponse
from src.db.models import OrderDB

from src.common.types_ import RedisMapping


def map_order_from_db(order_db: OrderDB) -> OrderDataSchema:
    return OrderDataSchema(
        id=order_db.id,
        items=order_db.items,
        total_price=order_db.total_price,
        status=order_db.status,
        user_id=order_db.user_id,
        created_at=order_db.created_at,
    )


def map_orders_from_db(db_orders: Sequence[OrderDB]) -> UserOrdersGetResponse:
    # внутри энивей такая же итерация
    # но мб можно через TypeAdapter это куда то в ядро пудантика закинуть
    return UserOrdersGetResponse(
        orders=[map_order_from_db(order) for order in db_orders]
    )


def map_order_schema_to_redis(order: OrderDataSchema) -> RedisMapping:
    mapping = order.model_dump()
    mapping["items"] = json.dumps(mapping["items"])
    mapping["total_price"] = str(mapping["total_price"])
    mapping["id"] = str(mapping["id"])
    mapping["user_id"] = str(mapping["user_id"])
    mapping["created_at"] = order.created_at.isoformat()
    return mapping


def map_order_schema_from_redis(order_map: RedisMapping) -> OrderDataSchema:
    items = order_map["items"]
    if not isinstance(items, str):
        raise RuntimeError("items is not str")

    order_map["items"] = json.loads(items)
    return OrderDataSchema(**typing.cast(dict, order_map))
