# Most of this taken from Redowan Delowar's post on configurations with Pydantic
# https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    SECRET_KEY: str
    SENTRY_DSN: str | None = None

class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False
    MAILGUN_DOMAIN: Optional[str] = None
    MAILGUN_API_KEY: Optional[str] = None
    LOGTAIL_API_KEY: Optional[str] = None
    B2_KEY_ID: Optional[str] = None
    B2_APPLICATION_KEY: Optional[str] = None
    B2_BUCKET_NAME: Optional[str] = None
    DEEPAI_API_KEY: Optional[str] = None
    SENTRY_DSN:Optional[str] = None


class DevConfig(BaseConfig):
    ENVIRONMENT: str = "development"


class ProdConfig(BaseConfig):
    ENVIRONMENT: str = "production"


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache()
def get_config(env_state: str):
    """Instantiate config based on the environment."""
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE or "dev")
if config.ENV_STATE == "prod" and (
    not config.DATABASE_URL or not config.DATABASE_URL.startswith("postgresql")
):
    raise RuntimeError("Production must use PostgreSQL DATABASE_URL")
print("ENV:", BaseConfig().ENV_STATE)
print("DB:", config.DATABASE_URL)