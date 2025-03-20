from pydantic import RedisDsn
from pydantic_settings import BaseSettings


class _RedisConfig(BaseSettings):
    redis_url: RedisDsn
