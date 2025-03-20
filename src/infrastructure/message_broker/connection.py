from __future__ import annotations

from aio_pika import connect_robust, Message as MessageMQ
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractChannel,
    AbstractExchange,
)

from src.common.initializer import Initialized
from src.core.config.compilation import MessageBrokerConfig
from src.core.constants.message_broker import MessageBrokerConstants
from src.schemas.message import BrokerMessageSchema


class RabbitConnection(Initialized):
    def __init__(
        self,
        connection: AbstractRobustConnection,
        channel: AbstractChannel,
        exchange: AbstractExchange,
    ):
        self.connection = connection
        self.channel = channel
        self.exchange = exchange

    async def disconnect(self) -> None:
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

        self.initialized = None

    @classmethod
    async def run_initialize(cls) -> RabbitConnection:
        connection = await connect_robust(
            MessageBrokerConfig.rabbitmq_url.unicode_string(),
            timeout=MessageBrokerConstants.connect_timeout_seconds,
        )
        channel = await connection.channel(publisher_confirms=False)
        exchange = await channel.declare_exchange(
            MessageBrokerConstants.orders_exchange
        )
        return cls(connection=connection, channel=channel, exchange=exchange)

    async def send_messages(
        self,
        messages: list[BrokerMessageSchema],
        *,
        routing_key: str = MessageBrokerConstants.queue,
    ) -> None:
        async with self.channel.transaction():
            for message in messages:
                mq_message = MessageMQ(body=message.model_dump_json().encode())
                await self.exchange.publish(
                    mq_message,
                    routing_key=routing_key,
                )

    async def send_message(
        self,
        message: BrokerMessageSchema,
        *,
        routing_key: str = MessageBrokerConstants.queue,
    ) -> None:
        async with self.channel.transaction():
            mq_message = MessageMQ(body=message.model_dump_json().encode())
            await self.exchange.publish(
                mq_message,
                routing_key=routing_key,
            )


rabbit_connection = RabbitConnection.uninitialized()
