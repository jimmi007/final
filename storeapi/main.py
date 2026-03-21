import logging
import os
from contextlib import asynccontextmanager

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from storeapi.config import config
from storeapi.database import database, engine, metadata
from storeapi.routers.post import router as post_router
from storeapi.routers.upload import router as upload_router
from storeapi.routers.user import router as user_router


# LOGGING -> να φαίνονται στο Render
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("storeapi")


# SENTRY
if config.SENTRY_DSN:
    sentry_sdk.init(
        dsn="https://b3240e57caf43a4a6212572c66ecbfad@o4511077739397120.ingest.de.sentry.io/4511083349803088",
        integrations=[FastApiIntegration()],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    logger.info("Sentry initialized")
else:
    logger.info("Sentry NOT initialized")


# DB lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting app...")
    logger.info(f"ENV_STATE: {config.ENV_STATE}")
    logger.info(f"DATABASE_URL exists: {config.DATABASE_URL is not None}")

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


@app.get("/sentry-debug")
async def trigger_error():
    1 / 0


@app.get("/log-test")
def log_test():
    logger.debug("DEBUG log")
    logger.info("INFO log")
    logger.warning("WARNING log")
    logger.error("ERROR log")
    return {"ok": True}


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)