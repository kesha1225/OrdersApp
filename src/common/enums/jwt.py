import enum


@enum.unique
class JwtKey(enum.StrEnum):
    expire = "exp"
    user_email = "sub"
