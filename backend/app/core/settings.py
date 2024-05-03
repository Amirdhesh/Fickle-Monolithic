from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_URI: str = os.environ.get("postgres_uri")
    JWT_ALGORITHM: str = os.environ.get("jwt_algorithm")
    JWT_SECRET_KEY: str = os.environ.get("jwt_secret_key")
    JWT_EXPIRY_TIME: int = os.environ.get("jwt_expiry_time")
    SENDER_EMAIL: str = os.environ.get("sender_email")
    SENDER_EMAIL_PASSWORD: str = os.environ.get("sender_email_password")
    REDIS_HOST: str = os.environ.get("redis_host")
    REDIS_PORT: str = os.environ.get("redis_port")
    REDIS_DB: int = os.environ.get("redis_database")
    CELERY_BROKER: str = os.environ.get("celery_broker")
    CELERY_BACKEND: str = os.environ.get("celery_backend")
    LOGGING_INI: str = "logging.ini"
    LOG_FILE_NAME: str = "fickle.log"
    LOG_FILE_SIZE: str = os.environ.get("log_file_size")
    LOG_FILE_BACKUP: str = os.environ.get("log_file_backup")
    LOGGING_PLATFORM_TOKEN: str = os.environ.get("betterstack_token")



settings = Settings()
