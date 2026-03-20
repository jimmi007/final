import logging
from contextlib import asynccontextmanager
import sentry_sdk
from sentry_sdk.integrations.asgi  import SentryAsgiMiddleware
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from sentry_sdk.integrations.fastapi import FastApiIntegration

from storeapi.config import config
from storeapi.database import database, engine, metadata
from storeapi.logging_conf import configure_logging
from storeapi.routers.post import router as post_router
from storeapi.routers.upload import router as upload_router
from storeapi.routers.user import router as user_router

logger = logging.getLogger(__name__)

sentry_sdk.init(
    dsn="https://03595b71cc1809e83351a8fb21935173@o4511077739397120.ingest.de.sentry.io/4511077742870608",
    integrations=[FastApiIntegration(), ],
    traces_sample_rate=1.0,
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info

)
@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    metadata.create_all(engine)
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.add_middleware(CorrelationIdMiddleware)

app.include_router(post_router)
app.include_router(upload_router)
app.include_router(user_router)

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
    return division_by_zero
    # response={"mistake":"division error"}
    # logger(f"its mistake")
    # return response

@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)


print(config.B2_BUCKET_NAME)
print(config.DATABASE_URL)