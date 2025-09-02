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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
