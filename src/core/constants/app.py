from src.core.config.compilation import APP_CONFIG


class AppConstants:
    db_url: str = (
        f"postgresql+asyncpg://{APP_CONFIG.postgres_user}"
        f":{APP_CONFIG.postgres_password}@postgres:5432/{APP_CONFIG.postgres_db}"
    )

    max_password_length: int = 100
    max_email_length: int = 100
