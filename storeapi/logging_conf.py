import logging
<<<<<<< HEAD
from logging.config import dictConfig

from storeapi.config import DevConfig, ProdConfig, config

def obfuscated(email: str, obfuscated_length: int) -> str:
    if not isinstance(email, str) or "@" not in email:
        return str(email)

    first, last = email.split("@", 1)
    visible = first[:obfuscated_length]
    return visible + ("*" * max(len(first) - obfuscated_length, 0)) + "@" + last
=======
import os
from logging.config import dictConfig

from storeapi.config import config


def obfuscated(email: str, obfuscated_length: int) -> str:
    first, last = email.split("@")
    visible = first[:obfuscated_length]
    return visible + ("*" * (len(first) - obfuscated_length)) + "@" + last

>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc

class EmailObfuscationFilter(logging.Filter):
    def __init__(self, name: str = "", obfuscated_length: int = 2) -> None:
        super().__init__(name)
        self.obfuscated_length = obfuscated_length

    def filter(self, record: logging.LogRecord) -> bool:
<<<<<<< HEAD
        if "email" in record.__dict__:
=======
        if hasattr(record, "email"):
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
            record.email = obfuscated(record.email, self.obfuscated_length)
        return True


<<<<<<< HEAD
handlers = ["default", "rotating_file"]
if isinstance(config, ProdConfig):
    handlers = ["default", "rotating_file", "logtail"]


def configure_logging() -> None:
=======
def configure_logging():
    is_prod = config.ENVIRONMENT == "production"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
<<<<<<< HEAD
                    "uuid_length": 8 if isinstance(config, DevConfig) else 32,
=======
                    "uuid_length": 32 if is_prod else 8,
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
                    "default_value": "-",
                },
                "email_obfuscation": {
                    "()": EmailObfuscationFilter,
<<<<<<< HEAD
                    "obfuscated_length": 2 if isinstance(config, DevConfig) else 0,
=======
                    "obfuscated_length": 0 if is_prod else 2,
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
<<<<<<< HEAD
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s %(msecs)03d %(levelname)s %(correlation_id)s %(name)s %(lineno)d %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"]
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": "storeapi.log",
                    "maxBytes": 1024 * 1024,  # 1MB
                    "backupCount": 5,
                    "encoding": "utf8",
                    "filters": ["correlation_id", "email_obfuscation"]
                },
                "logtail": {
                    "class": "logtail.LogtailHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
                    "source_token": config.LOGTAIL_API_KEY
                }
            },
            "loggers": {
                "uvicorn": {"handlers": ["default", "rotating_file"], "level": "INFO"},
                "storeapi": {
                    "handlers": handlers,
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False
                },
                "databases": {"handlers": ["default"], "level": "WARNING"},
                "aiosqlite": {"handlers": ["default"], "level": "WARNING"}
            }
        }
    )
=======
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(asctime)s | %(levelname)s | %(correlation_id)s | %(name)s:%(lineno)d | %(message)s",
                },
                "json": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(levelname)s %(correlation_id)s %(name)s %(lineno)d %(message)s",
                },
            },
            "handlers": {
                # Αυτό βλέπει το Render
                "console": {
                    "class": "logging.StreamHandler",
                    "level": LOG_LEVEL,
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
                    "stream": "ext://sys.stdout",
                },
                # File logs (μόνο local ή αν έχεις disk)
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "INFO",
                    "formatter": "json",
                    "filename": "storeapi.log",
                    "maxBytes": 1024 * 1024,
                    "backupCount": 5,
                    "encoding": "utf8",
                    "filters": ["correlation_id", "email_obfuscation"],
                },
            },
            "root": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
            },
            "loggers": {
                "uvicorn": {
                    "level": "WARNING",
                    "propagate": False,
                },
                "uvicorn.error": {
                    "level": "ERROR",
                    "propagate": False,
                },
                "uvicorn.access": {
                    "level": "WARNING",
                    "propagate": False,
                },
                "sqlalchemy.engine": {
                    "level": "WARNING",
                    "propagate": False,
                },
                "sentry_sdk": {
                    "level": "ERROR",
                    "propagate": False,
                },
                "storeapi": {
                    "handlers": ["console", "file"] if is_prod else ["console"],
                    "level": "INFO" if is_prod else "DEBUG",
                    "propagate": False,
                },
            },
        }
    )


>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
