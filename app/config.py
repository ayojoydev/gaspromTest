import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@db:5432/device_analytics"
    )
    
    # Redis & Celery
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/1")
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/2")
    
    # API
    api_title: str = "Device Analytics Service"
    api_version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG", "False") == "True"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
