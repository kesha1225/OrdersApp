from pydantic import JsonValue
from src.common.enums.action import ActionType

from src.schemas.base import BaseSchema


class BrokerMessageSchema(BaseSchema):
    action: ActionType
    body: dict[str, JsonValue]
