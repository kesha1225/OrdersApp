import json

from src.common.enums.action import ActionType

from src.schemas.message import BrokerMessageSchema
from src.schemas.order import OrderDataSchema


def create_new_order_message(order: OrderDataSchema) -> BrokerMessageSchema:
    # Decimal and UUID is not json serializable
    return BrokerMessageSchema(
        action=ActionType.new_order, body=json.loads(order.model_dump_json())
    )
