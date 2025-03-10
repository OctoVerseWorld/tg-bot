import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator, TypedDict

import ngrok
import sentry_sdk
from aiogram import Bot
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from src.application.uow.uow import IUnitOfWork
from src.config.app import app_settings
from src.config.server import server_settings
from src.config.tg_api import tg_api_settings
from src.infrastructure.aiogram.tg_bot import create_bot, create_dispatcher
from src.ui.rest_api import router as api_router


async def start_ngrok_tunnel(queue):
    session = await ngrok.SessionBuilder().authtoken_from_env().connect()
    ngrok_listener = await session.http_endpoint().listen()
    queue.put_nowait(ngrok_listener.url())
    await ngrok_listener.forward(f"localhost:{server_settings.PORT}")


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    # Database healthcheck
    from src.infrastructure.database.base import engine
    from src.infrastructure.database.healthcheck import healthcheck as db_healthcheck
    await db_healthcheck()

    bot = await create_bot()
    IUnitOfWork.bot = bot
    dp = await create_dispatcher(bot, app_)
    if app_settings.ENVIRONMENT == 'local_development':
        logging.info("Starting the ngrok tunnel...")
        queue = asyncio.Queue()
        asyncio.create_task(start_ngrok_tunnel(queue))
        ngrok_url = await queue.get()
        webhook_url = ngrok_url + tg_api_settings.WEBHOOK_PATH
    else:
        webhook_url = app_settings.URL + tg_api_settings.WEBHOOK_PATH
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != webhook_url:
        await bot.set_webhook(
            url=webhook_url,
            secret_token=tg_api_settings.WEBHOOK_SECRET,
        )

    try:
        yield
    finally:
        # Shutdown events
        await engine.dispose()  # Clean up the connection pool
        await bot.session.close()  # Close the aiohttp session


def create_app() -> FastAPI:
    sentry_sdk.init(
        dsn="https://c1fa741ba5005563f753fbae9a5dc180@o4508952916983808.ingest.de.sentry.io/4508952918556752",
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
    )

    app_ = FastAPI(
        title="TG Bot Service",
        version="1.0.0",
        lifespan=lifespan,
        docs_url=None if app_settings.ENVIRONMENT == 'production' else "/docs",
        redoc_url=None if app_settings.ENVIRONMENT == 'production' else "/redoc",
        openapi_url=None if app_settings.ENVIRONMENT == 'production' else "/openapi.json",
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[],
    )

    app_.get("/metrics")(lambda _: Response(status_code=status.HTTP_204_NO_CONTENT))

    app_.include_router(api_router)
    return app_
