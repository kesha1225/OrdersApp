import datetime
from typing import Annotated
from fntypes import Ok, Error

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.api.dependencies import get_auth_service
from src.schemas.token import JwtTokenResponse
from src.schemas.user import UserRegister, UserBaseResponse
from src.common.enums.jwt import JwtKey
from src.core.constants.api import ApiConstants
from src.core.security import create_access_token
from src.services.user import UserService

router = APIRouter(prefix=ApiConstants.auth_prefix)


@router.post(
    ApiConstants.register_prefix,
    response_model=UserBaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserRegister,
    user_service: Annotated[UserService, Depends(get_auth_service)],
):
    match await user_service.register(user_register=user_data):
        case Ok(user):
            return UserBaseResponse(id=user.id)
        case Error(error):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


@router.post(ApiConstants.token_prefix, response_model=JwtTokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_auth_service)],
):
    authenticated_user = await user_service.authenticate(
        email=form_data.username, password=form_data.password
    )
    match authenticated_user:
        case Ok(user):
            access_token_expires = datetime.timedelta(
                minutes=ApiConstants.access_token_expire_minutes
            )
            access_token = create_access_token(
                data={JwtKey.user_email: user.email}, expires_delta=access_token_expires
            )
            return JwtTokenResponse(access_token=access_token)
        case Error(error):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error,
                headers=ApiConstants.bearer_headers,
            )
