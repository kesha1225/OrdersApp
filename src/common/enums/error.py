import enum
from typing import Any, Self

from fntypes import Error


class BaseErrorEnum(enum.StrEnum):
    def __call__(self, _: Any, /) -> Error[Self]:
        return Error(self)


@enum.unique
class UserError(BaseErrorEnum):
    not_found = "user not found"
    already_exists = "user already exists"
    cant_create = "cant create user"
    invalid_password = "invalid password"
    bad_auth = "incorrect auth data"


@enum.unique
class TokenError(BaseErrorEnum):
    expired = "token expired"
    bad = "bad token"
    no_email = "no email in token"


@enum.unique
class AuthError(BaseErrorEnum):
    cant_auth = "cant process auth"


@enum.unique
class OrderError(BaseErrorEnum):
    cant_create = "cant create order"
    not_found = "order not found"


@enum.unique
class RedisError(BaseErrorEnum):
    not_found = "key not_found"
