import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: str = "dev"
    DATABASE_URL: str
    SECRET_KEY: str
    SENTRY_DSN: Optional[str] = None
    DB_FORCE_ROLL_BACK:bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DevConfig(BaseConfig):
    DATABASE_URL: str = os.getenv("DEV_DATABASE_URL")
    SENTRY_DSN: Optional[str] = os.getenv("DEV_SENTRY_DSN")
    DB_FORCE_ROLL_BACK: bool =os.getenv("DEV_DB_FORCE_ROLL_BACK", False)==True

class ProdConfig(BaseConfig):
    DATABASE_URL: str = os.getenv("PROD_DATABASE_URL")
    SENTRY_DSN: Optional[str] = os.getenv("PROD_SENTRY_DSN")
    DB_FORCE_ROLL_BACK: bool = os.getenv("PROD_DB_FORCE_ROLL_BACK", False) == True


@lru_cache()
def get_config():
    env_state = os.getenv("ENV_STATE", "dev")

    if env_state == "prod":
        return ProdConfig()
    else:
        return DevConfig()


config = get_config()