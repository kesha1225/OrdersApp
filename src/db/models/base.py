import datetime
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    validates,
    declared_attr,
    orm_insert_sentinel,
    DeclarativeBase,
)

from src.common.times import get_utcnow
from src.db.extensions.datetime_utc import DateTimeUTC


class ServerDefault:
    true = "true"
    false = "false"
    empty_dict = "{}"
    now = text("CURRENT_TIMESTAMP")
    uuid = text("gen_random_uuid()")


class OnDelete:
    cascade = "CASCADE"
    set_null = "SET NULL"
    restrict = "RESTRICT"


class UUIDBase:
    id: Mapped[UUID] = mapped_column(
        default=uuid4, primary_key=True, server_default=ServerDefault.uuid
    )
    """UUID Primary key column."""

    @declared_attr
    def _sentinel(cls) -> Mapped[int]:
        return orm_insert_sentinel(name="sa_orm_sentinel")


class ModelBase(DeclarativeBase, AsyncAttrs):
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=get_utcnow,
        server_default=ServerDefault.now,
    )
    """Date/time of instance creation."""
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=get_utcnow,
        server_default=ServerDefault.now,
        onupdate=get_utcnow,
        server_onupdate=ServerDefault.now,
    )
    """Date/time of instance last update."""

    @validates("created_at", "updated_at")
    def validate_tz_info(self, _: str, value: datetime.datetime) -> datetime.datetime:
        if value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value
