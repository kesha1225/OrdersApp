import asyncio
import json

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from src.core.config.compilation import MessageBrokerConfig
from src.core.constants.message_broker import MessageBrokerConstants
from src.core.tasks.order import process_order_task
from src.schemas.message import BrokerMessageSchema


async def process_message(raw_message: AbstractIncomingMessage) -> None:
    async with raw_message.process():
        message = BrokerMessageSchema(**json.loads(raw_message.body.decode()))
        print(
            f"Processing message in consumer... {message.action} {message.body['id']}"
        )
        process_order_task.delay(message.body)


async def run_consumer() -> None:
    connection = await aio_pika.connect_robust(
        MessageBrokerConfig.rabbitmq_url.unicode_string()
    )
    channel = await connection.channel(publisher_confirms=False)
    await channel.set_qos(
        prefetch_count=MessageBrokerConstants.max_tasks_consumer_count
    )
    queue = await channel.declare_queue(MessageBrokerConstants.queue)

    exchange = await channel.declare_exchange(MessageBrokerConstants.orders_exchange)
    await queue.bind(exchange, MessageBrokerConstants.queue)
    await queue.consume(process_message)
    try:
        await asyncio.Future()
    finally:
        await connection.close()
