from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()