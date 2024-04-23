from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    DB_URI : str = os.environ.get('postgres_uri')
    JWT_ALGORITHM = "HS256"
    JWT_SECRET_KEY = "dtyuilmnbvftyuik09876tghj6456yhfdsw234rg6rthg7kg5rtyujgyuji876rfv"




settings = Settings()