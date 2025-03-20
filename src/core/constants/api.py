from fastapi.security import OAuth2PasswordBearer

from src.common.types_ import Headers


class ApiConstants:
    access_token_expire_minutes: int = 10
    base_access_token_expire_minutes: int = 15

    api_prefix: str = "/api"

    auth_prefix: str = "/auth"
    oauth2_prefix: str = "api/auth/token"
    token_prefix: str = "/token"
    register_prefix: str = "/register"

    orders_prefix: str = "/orders"
    create_order_prefix: str = "/"
    order_id_prefix: str = "/{order_id}"
    user_orders_prefix: str = "/user/{user_id}"

    jwt_algorithm: str = "HS256"

    bearer_headers: Headers = {"WWW-Authenticate": "Bearer"}
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl=oauth2_prefix)

    request_per_second_limit: int = 5
    
    allowed_origins: list[str] = ["*"]
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]
