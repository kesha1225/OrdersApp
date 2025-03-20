from uuid import UUID

from pydantic import EmailStr, Field

from src.schemas.base import BaseSchema
from src.core.constants.app import AppConstants


class UserRegister(BaseSchema):
    email: EmailStr = Field(..., max_length=AppConstants.max_email_length)
    password: str = Field(..., max_length=AppConstants.max_password_length)


class UserBaseResponse(BaseSchema):
    id: UUID
