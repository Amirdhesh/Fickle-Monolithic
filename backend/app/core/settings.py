from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URI: str 
    TEST_DB_URI: str 
    JWT_ALGORITHM: str 
    JWT_SECRET_KEY: str 
    JWT_EXPIRY_TIME: int 
    SENDER_EMAIL: str 
    SENDER_EMAIL_PASSWORD: str 
    REDIS_HOST: str 
    REDIS_PORT: str 
    REDIS_DB: int 
    CELERY_BROKER: str 
    CELERY_BACKEND: str 
    
    class Config:
        env_file = ".env"


settings = Settings()
