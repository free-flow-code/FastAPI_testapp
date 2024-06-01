from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled"
        ]
)

# celery.conf.timezone = 'UTC'

celery.conf.beat_schedule = {
    "send-remind-one-day-email": {
        "task": "send_tomorrow_reservation_email",
        "schedule": crontab(hour=9, minute=0),
    },
    "send-remind-tree-days-email": {
        "task": "send_three_days_reservation_email",
        "schedule": crontab(hour=15, minute=30),
    }
}
