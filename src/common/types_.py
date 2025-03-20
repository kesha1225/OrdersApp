import typing
from typing import Literal, Any

from fntypes import Result

from src.common.enums.error import BaseErrorEnum, RedisError
from src.db.models import UserDB, OrderDB

if typing.TYPE_CHECKING:
    from src.schemas.order import OrderDataSchema

type UserDbResult = Result[UserDB, BaseErrorEnum]
type OrderDbResult = Result[OrderDB, BaseErrorEnum]
type OrderSchemaResult = Result[OrderDataSchema, BaseErrorEnum]
type UpdateOrderDbResult = Result[Literal[True], BaseErrorEnum]

type JwtData = dict[str, str]
type JwtDecodeResult = Result[JwtData, BaseErrorEnum]
type Headers = dict[str, str]

type OrderItems = dict[str, int]

type OrderCacheGetResult = Result["OrderDataSchema", RedisError]


type RedisMapping = dict[str, bytes | str | int | float | Any]
