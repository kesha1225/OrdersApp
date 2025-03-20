import typing
from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.enums.order import OrderStatus
from src.db.models.base import ModelBase, UUIDBase, OnDelete, ServerDefault

if typing.TYPE_CHECKING:
    from src.db.models.user import UserDB


class OrderDB(ModelBase, UUIDBase):
    __tablename__ = "order"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("userdb.id", ondelete=OnDelete.cascade)
    )

    items: Mapped[dict] = mapped_column(
        JSONB, default={}, server_default=ServerDefault.empty_dict
    )
    total_price: Mapped[Decimal]
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.pending)

    user: Mapped["UserDB"] = relationship(back_populates="orders")
