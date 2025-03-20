from src.schemas.base import BaseSchema


class JwtTokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"
