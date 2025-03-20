from celery import Celery

from src.core.config.compilation import MessageBrokerConfig
from src.core.constants.celery import CeleryConstants

celery_app = Celery(
    CeleryConstants.worker_name,
    broker=MessageBrokerConfig.rabbitmq_url.unicode_string(),
)

celery_app.conf.imports = [
    "src.core.tasks",
]
