from pydantic_settings import BaseSettings


class _ApiConfig(BaseSettings):
    jwt_secret: str
