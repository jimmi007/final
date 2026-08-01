import logging
from contextlib import asynccontextmanager

import sentry_sdk
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from sentry_sdk.integrations.fastapi import FastApiIntegration

from storeapi.config import config
from storeapi.database import database, engine, metadata
from storeapi.routers.post import router as post_router
from storeapi.routers.upload import router as upload_router
from storeapi.routers.user import router as user_router
import os

print("MAIN:", __file__, flush=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("storeapi")


sentry_dsn = getattr(config, "SENTRY_DSN", None)

if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[FastApiIntegration()],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    logger.info("Sentry initialized")
else:
    logger.info("Sentry not initialized")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    logger.info("ENV_STATE: %s", config.ENV_STATE)
    logger.info("DATABASE_URL exists: %s", bool(config.DATABASE_URL))

    metadata.create_all(engine)

    await database.connect()
    logger.info("Database connected")

    yield

    await database.disconnect()
    logger.info("Database disconnected")


app = FastAPI(lifespan=lifespan)

app.add_middleware(CorrelationIdMiddleware)

app.include_router(post_router)
app.include_router(upload_router)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "API is running"}


@app.get("/log-test")
async def log_test():
    logger.info("INFO log from Render")
    logger.warning("WARNING log from Render")
    logger.error("ERROR log from Render")

    return {"ok": True}


@app.get("/sentry-debug")
async def trigger_error():
    division = 1 / 0
    return {"result": division}


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(
        "HTTPException: %s %s",
        exc.status_code,
        exc.detail,
    )
    return await http_exception_handler(request, exc)