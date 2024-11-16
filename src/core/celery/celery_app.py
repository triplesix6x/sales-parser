import logging
import logging.config
import yaml
from celery import Celery
from celery.schedules import crontab
from core.config import settings
from celery.signals import after_setup_logger


celery_app = Celery(
    "app",
    broker=settings.rabbitmq.brocker,
    backend=settings.rabbitmq.backend,
    include=["core.celery.tasks"],
)

celery_app.conf.beat_schedule = {
    "process_sales_data_daily_at_noon": {
        "task": "core.celery.tasks.process_sales_data",
        "schedule": crontab(hour=12, minute=0),
        "args": (),
    },
}
celery_app.conf.timezone = "Europe/Moscow"


logger = logging.getLogger(__name__)

with open("log_conf.yaml", 'r') as f:
    log_config = yaml.safe_load(f.read())


@after_setup_logger.connect
def setup_loggers(*args, **kwargs):
    logging.config.dictConfig(log_config)
