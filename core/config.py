from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # تحميل المتغيرات من .env

class Settings(BaseSettings):
    PROJECT_NAME: str = "TopicX Beta"
    DATABASE_URL: str
    SECRET_KEY: str = "19a0692f9fed9914371cb6f5a25d2ff28da356d595796da8c8086b1450964a87"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    DEBUG: bool = False
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REFRESH_SECRET_KEY: str = "891eee28617250bae903d2a030d944c989e2c5ac643a0c811b0bfb896150f538"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
