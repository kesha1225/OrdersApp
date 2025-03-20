from typing import AsyncGenerator, Annotated, NoReturn

from fastapi import Depends, HTTPException
from fntypes import Ok, Error
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.common.enums.error import AuthError
from src.core.constants.api import ApiConstants
from src.db.models import UserDB
from src.db.session import ASYNC_SESSION
from src.repository.abstract.order import AbstractOrderRepository
from src.repository.abstract.user import AbstractUserRepository
from src.repository.alchemy.order import AlchemyOrderRepository
from src.repository.alchemy.user import AlchemyUserRepository
from src.services.order import OrderService
from src.services.user import UserService


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with ASYNC_SESSION() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AbstractUserRepository:
    return AlchemyUserRepository(session=session)


async def get_order_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AbstractOrderRepository:
    return AlchemyOrderRepository(session=session)


async def get_order_service(
    order_repository: Annotated[AbstractOrderRepository, Depends(get_order_repository)],
) -> OrderService:
    return OrderService(user_repository=order_repository)


async def get_auth_service(
    user_repository: Annotated[AbstractUserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(user_repository=user_repository)


async def get_authenticated_user_di(
    user_service: Annotated[UserService, Depends(get_auth_service)],
    token: Annotated[str, Depends(ApiConstants.oauth2_scheme)],
) -> UserDB | NoReturn:
    match await user_service.get_from_jwt_token(token=token):
        case Ok(user):
            return user
        case Error(error):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error,
                headers=ApiConstants.bearer_headers,
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=AuthError.cant_auth,
                headers=ApiConstants.bearer_headers,
            )
