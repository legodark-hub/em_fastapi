import logging
from celery import Celery
from celery.schedules import crontab
import redis

from config import REDIS_HOST, REDIS_PORT

redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}"

celery_app = Celery(
    "tasks",
    broker=redis_url,  
)

redis_client = redis.from_url(redis_url)

@celery_app.task
def clear_cache():
    redis_client.flushdb()

    
celery_app.conf.beat_schedule = {
    "clear-cache-every-day": {
        "task": "celery_app.clear_cache",
        "schedule": crontab(hour='14', minute='11'),
    },
}

celery_app.autodiscover_tasks()
