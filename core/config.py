from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # تحميل المتغيرات من .env

class Settings(BaseSettings):
    PROJECT_NAME: str = "TopicX Beta"
    DATABASE_URL: str
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DEBUG: bool = False
    REFRESH_TOKEN_EXPIRE_DAYS: int = 3
    REFRESH_SECRET_KEY: str = "supersecret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
