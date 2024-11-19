from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 1200)

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


env_settings = Settings
