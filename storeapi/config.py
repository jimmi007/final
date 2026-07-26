<<<<<<< HEAD
# Most of this taken from Redowan Delowar's post on configurations with Pydantic
# https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


# Most of this taken from Redowan Delowar's post on configurations with Pydantic
# https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html
=======
import os
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: str = "dev"
<<<<<<< HEAD

    """Loads the dotenv file. Including this is necessary to get
    pydantic to load a .env file."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


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

# Η βάση globalconfig για όλες τις κλάσεις.

class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache()
def get_config(env_state: str):
    """Instantiate config based on the environment."""
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()

# DevConfig(ανάπτυξη)
# ProdConfig(παραγωγή)
# TestConfig(για τεστ)


config = get_config(BaseConfig().ENV_STATE )
=======
    SECRET_KEY: str
    DATABASE_URL: str
    SENTRY_DSN: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False

    # GLOBAL
    LOG_LEVEL: str = "INFO"
    LOGTAIL_API_KEY: Optional[str] = None
    B2_BUCKET_NAME: Optional[str] = None
    B2_APPLICATION_KEY: Optional[str] = None
    B2_KEY_ID: Optional[str] = None
    MAILGUN_API_KEY: Optional[str] = None
    MAILGUN_DOMAIN: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DevConfig(BaseConfig):
    DATABASE_URL: str = os.getenv("DEV_DATABASE_URL")
    SENTRY_DSN: Optional[str] = os.getenv("DEV_SENTRY_DSN")
    DB_FORCE_ROLL_BACK: bool = os.getenv("DEV_DB_FORCE_ROLL_BACK", "False") == "True"


class ProdConfig(BaseConfig):
    DATABASE_URL: str = os.getenv("PROD_DATABASE_URL")
    SENTRY_DSN: Optional[str] = os.getenv("PROD_SENTRY_DSN")
    DB_FORCE_ROLL_BACK: bool = os.getenv("PROD_DB_FORCE_ROLL_BACK", "False") == "True"
    LOGTAIL_API_KEY: Optional[str] = os.getenv("PROD_LOGTAIL_API_KEY")
    B2_BUCKET_NAME: Optional[str] = os.getenv("PROD_B2_BUCKET_NAME")
    B2_APPLICATION_KEY: Optional[str] = os.getenv("PROD_B2_APPLICATION_KEY")
    B2_KEY_ID: Optional[str] = os.getenv("PROD_B2_KEY_ID")
    MAILGUN_API_KEY: Optional[str] = os.getenv("PROD_MAILGUN_API_KEY")
    MAILGUN_DOMAIN: Optional[str] = os.getenv("PROD_MAILGUN_DOMAIN")


@lru_cache()
def get_config():
    env_state = os.getenv("ENV_STATE", "dev")

    if env_state == "prod":
        return ProdConfig()
    else:
        return DevConfig()


config = get_config()
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
