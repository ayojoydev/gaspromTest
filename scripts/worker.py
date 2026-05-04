import os
import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from app.tasks.celery_app import celery_app
from app.tasks.analytics import *  # noqa: F401, F403

if __name__ == "__main__":
    celery_app.start()
