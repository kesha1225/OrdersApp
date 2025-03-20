import asyncio

from src.db.models import OrderDB
from src.infrastructure.message_broker.connection import rabbit_connection
from src.infrastructure.message_broker.message_fabric import create_new_order_message
from src.infrastructure.redis.order import redis_cache
from src.schemas.mappers.order import map_order_from_db


async def post_create_order_actions(new_order: OrderDB) -> None:
    # event driven потенциальный
    mapped_order = map_order_from_db(order_db=new_order)
    asyncio.create_task(
        rabbit_connection.send_message(
            message=create_new_order_message(order=mapped_order)
        )
    )
    asyncio.create_task(redis_cache.set_order(order=mapped_order))
