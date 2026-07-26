import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

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

    await database.connect()
    logger.info("Database connected")

    yield

    logger.info("Disconnecting database...")
    await database.disconnect()
    logger.info("Database disconnected")


app = FastAPI(lifespan=lifespan)

app.add_middleware(CorrelationIdMiddleware)

app.include_router(post_router)
app.include_router(user_router)
app.include_router(new_router)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)