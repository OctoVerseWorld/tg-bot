from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from fastapi import FastAPI

from src.config.tg_api import tg_api_settings
from src.ui.tg_api import router as tg_api_router


async def create_bot():
    return Bot(token=tg_api_settings.TOKEN, session=AiohttpSession())


async def create_dispatcher(bot: Bot, app: FastAPI):
    dp = Dispatcher(bot=bot)
    dp.include_router(tg_api_router)

    @app.post(tg_api_settings.WEBHOOK_PATH)
    async def bot_webhook(update: dict):
        await dp.feed_webhook_update(bot=bot, update=update)

    return dp
