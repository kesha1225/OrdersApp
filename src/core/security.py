import datetime

import bcrypt
import jwt

from fntypes import Ok, Error
from jwt import ExpiredSignatureError, PyJWTError

from src.common.enums.error import TokenError
from src.common.enums.jwt import JwtKey
from src.common.times import get_utcnow
from src.core.config.compilation import API_CONFIG
from src.common.types_ import JwtDecodeResult
from src.core.constants.api import ApiConstants


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_access_token(
    data: dict[str, str | datetime.datetime],
    expires_delta: datetime.timedelta | None = None,
) -> str:
    payload = data.copy()

    if expires_delta is None:
        expires_delta = datetime.timedelta(
            minutes=API_CONFIG.base_access_token_expire_minutes
        )

    expire = get_utcnow() + expires_delta

    payload[JwtKey.expire] = expire
    encoded_jwt = jwt.encode(
        payload, API_CONFIG.jwt_secret, algorithm=ApiConstants.jwt_algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> JwtDecodeResult:
    try:
        return Ok(
            jwt.decode(
                token, API_CONFIG.jwt_secret, algorithms=[ApiConstants.jwt_algorithm]
            )
        )
    except ExpiredSignatureError:
        return Error(TokenError.expired)
    except PyJWTError:
        return Error(TokenError.bad)
