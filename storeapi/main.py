import logging
<<<<<<< HEAD
from contextlib import asynccontextmanager

=======
import os
from contextlib import asynccontextmanager

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

<<<<<<< HEAD
from storeapi.database import database
from storeapi.logging_conf import configure_logging
from storeapi.routers.post import router as post_router
from storeapi.routers.user import router as user_router
from storeapi.routers.newfile import router as new_router
# Ρύθμιση logging
configure_logging()

logger = logging.getLogger("storeapi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting...")

=======
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
config.MAILGUN_API_KEY
config.MAILGUN_DOMAIN

# DB lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting app...")
    logger.info(f"ENV_STATE: {config.ENV_STATE}")
    logger.info(f"DATABASE_URL exists: {config.DATABASE_URL is not None}")

    metadata.create_all(engine)
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
    await database.connect()
    logger.info("Database connected")

    yield

<<<<<<< HEAD
    logger.info("Disconnecting database...")
=======
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
    await database.disconnect()
    logger.info("Database disconnected")


app = FastAPI(lifespan=lifespan)

app.add_middleware(CorrelationIdMiddleware)

app.include_router(post_router)
<<<<<<< HEAD
app.include_router(user_router)
app.include_router(new_router)
=======
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
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)