class MessageBrokerConstants:
    orders_exchange: str = "orders"
    connect_timeout_seconds: int = 3
    max_tasks_consumer_count: int = 100

    queue: str = "orders_q"
