from pydantic import AmqpDsn
from pydantic_settings import BaseSettings


class _MessageBrokerConfig(BaseSettings):
    rabbitmq_url: AmqpDsn
