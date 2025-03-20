import typing

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.core.constants.app import AppConstants
from src.db.models.base import ModelBase, UUIDBase

if typing.TYPE_CHECKING:
    from src.db.models.order import OrderDB


class UserDB(ModelBase, UUIDBase):
    __tablename__ = "userdb"

    email: Mapped[str] = mapped_column(
        String(length=AppConstants.max_email_length), unique=True
    )
    password: Mapped[str] = mapped_column(
        String(length=AppConstants.max_password_length)
    )

    orders: Mapped[list["OrderDB"]] = relationship(back_populates="user")
