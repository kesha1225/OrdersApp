from pydantic_settings import BaseSettings


class _AppConfig(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
