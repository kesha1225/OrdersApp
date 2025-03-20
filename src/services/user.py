from functools import partial

from fntypes import Error, Ok, Result

from src.common.fn import is_err
from src.schemas.user import UserRegister
from src.common.enums.error import UserError, TokenError
from src.common.enums.jwt import JwtKey
from src.core.security import hash_password, check_password, decode_token
from src.db.models import UserDB
from src.repository.abstract.user import AbstractUserRepository

from src.common.types_ import UserDbResult, JwtData


def get_authenticated_user(user: UserDB, password: str) -> UserDbResult:
    if not check_password(password=password, hashed_password=user.password):
        return Error(UserError.invalid_password)

    return Ok(user)


def get_email_from_jwt_token(jwt_data: JwtData) -> Result[str, TokenError]:
    email = jwt_data.get(JwtKey.user_email)
    if email is None:
        return Error(TokenError.no_email)

    return Ok(email)


class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def register(self, user_register: UserRegister) -> UserDbResult:
        return await self.user_repository.create(
            email=str(user_register.email),
            hashed_password=hash_password(user_register.password),
        )

    async def authenticate(self, email: str, password: str) -> UserDbResult:
        return (await self.user_repository.get_by_email(email=email)).and_then(
            partial(get_authenticated_user, password=password)
        )

    async def get_from_jwt_token(self, token: str) -> UserDbResult:
        email_result = decode_token(token=token).and_then(get_email_from_jwt_token)

        # waiting for async support in fntypes lib
        # https://github.com/timoniq/fntypes/issues/13
        if is_err(email_result):
            return email_result

        return await self.user_repository.get_by_email(email=email_result.value)
