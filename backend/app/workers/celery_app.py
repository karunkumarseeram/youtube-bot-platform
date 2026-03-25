"""
Celery Application Configuration
Python 3.14.3 Compatible
"""

from celery import Celery
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

celery_app = Celery(
    "youtube_bot",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

logger.info("✅ Celery app configured successfully")