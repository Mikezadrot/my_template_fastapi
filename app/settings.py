import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    DATABASE_USER: str
    DATABASE_PASS: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_PORT: int
    SECRET_KEY: str
    ACCESS_EXPIRE_MINUTES: int = 15
    REFRESH_EXPIRE_DAYS: int = 7
    DEBUG: bool = False

    DATABASE_URL: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DATABASE_URL = (
            f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASS}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

