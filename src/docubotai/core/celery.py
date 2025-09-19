"""
Celery configuration for DocuBotAI.
"""
from celery import Celery

# Create Celery app
celery_app = Celery(
    "docubot",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=[
        "docubot.tasks.scraping",
        "docubot.tasks.processing",
    ],
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1,
)