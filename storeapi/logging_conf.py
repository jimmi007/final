
import logging
from logging.config import dictConfig

from storeapi.config import DevConfig, ProdConfig, config


def obfuscated(email: str, obfuscated_length: int) -> str:
    characters = email[:obfuscated_length]
    first, last = email.split("@")
    return characters + ("*" * (len(first) - obfuscated_length)) + "@" + last


class EmailObfuscationFilter(logging.Filter):
    def __init__(self, name: str = "", obfuscated_length: int = 2) -> None:
        super().__init__(name)
        self.obfuscated_length = obfuscated_length

    def filter(self, record: logging.LogRecord) -> bool:
        if "email" in record.__dict__:
            record.email = obfuscated(record.email, self.obfuscated_length)
        return True


def configure_logging() -> None:
    is_prod = isinstance(config, ProdConfig)

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 32 if is_prod else 8,
                    "default_value": "-",
                },
                "email_obfuscation": {
                    "()": EmailObfuscationFilter,
                    "obfuscated_length": 0 if is_prod else 2,
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s | %(levelname)s | %(correlation_id)s | %(name)s:%(lineno)d | %(message)s",
                },
                "file": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s %(levelname)s %(correlation_id)s %(name)s %(lineno)d %(message)s",
                },
            },
            "handlers": {
                # IMPORTANT: Αυτό βλέπει το Render (stdout)
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
                    "stream": "ext://sys.stdout",
                },
                # Log file (μόνο για local/production storage)
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "INFO",
                    "formatter": "file",
                    "filename": "storeapi.log",
                    "maxBytes": 1024 * 1024,
                    "backupCount": 5,
                    "encoding": "utf8",
                    "filters": ["correlation_id", "email_obfuscation"],
                },
            },
            # ROOT logger (πολύ σημαντικό για Render)
            "root": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
            "loggers": {
                "uvicorn": {
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
                "storeapi": {
                    "handlers": ["console", "file"] if is_prod else ["console"],
                    "level": "INFO" if is_prod else "DEBUG",
                    "propagate": False,
                },
                "databases": {
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": False,
                },
                "aiosqlite": {
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": False,
                },
            },
        }
    )



