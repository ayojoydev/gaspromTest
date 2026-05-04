"""
Celery configuration module
"""

from app.tasks.celery_app import celery_app

# Import tasks to register them
from app.tasks.analytics import analyze_device_readings, analyze_user_devices

__all__ = [
    'celery_app',
    'analyze_device_readings',
    'analyze_user_devices',
]
