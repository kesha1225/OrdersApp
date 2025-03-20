from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.core.constants.app import AppConstants

ENGINE = create_async_engine(AppConstants.db_url)
ASYNC_SESSION = async_sessionmaker(
    bind=ENGINE, class_=AsyncSession, expire_on_commit=False
)
