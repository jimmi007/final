import logging
import os
from logging.config import dictConfig

from storeapi.config import config


def obfuscated(email: str, obfuscated_length: int) -> str:
    first, last = email.split("@")
    visible = first[:obfuscated_length]
    return visible + ("*" * (len(first) - obfuscated_length)) + "@" + last


class EmailObfuscationFilter(logging.Filter):
    def __init__(self, name: str = "", obfuscated_length: int = 2) -> None:
        super().__init__(name)
        self.obfuscated_length = obfuscated_length

    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, "email"):
            record.email = obfuscated(record.email, self.obfuscated_length)
        return True


def configure_logging():
    is_prod = config.ENV == "production"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

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


