import time

from celery.utils.log import get_task_logger

from src.core.celery_app import celery_app


logger = get_task_logger(__name__)


@celery_app.task
def process_order_task(raw_order_data: dict):
    time.sleep(2)
    logger.info(f"Order {raw_order_data['id']} processed")
