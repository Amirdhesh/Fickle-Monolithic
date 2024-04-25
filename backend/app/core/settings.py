from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    DB_URI : str = os.environ.get('postgres_uri')
    JWT_ALGORITHM : str = os.environ.get('jwt_algorithm')
    JWT_SECRET_KEY : str = os.environ.get('jwt_secret_key')
    SENDER_EMAIL : str = os.environ.get("sender_email")
    SENDER_EMAIL_PASSWORD : str = os.environ.get("sender_email_password")
    REDIS_HOST : str = os.environ.get("redis_host")
    REDIS_PORT : str = os.environ.get("redis_port")
    REDIS_DB : int = os.environ.get("redis_database")
    CELERY_BROKER : str = os.environ.get("celery_backend")


settings = Settings()