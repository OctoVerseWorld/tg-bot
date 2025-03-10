import logging
import time

from aiogram import Router, types, filters
from aiogram.exceptions import TelegramAPIError
from aiogram.utils import formatting

from src.application.uow.uow import IUnitOfWork
from src.application.use_cases.waitlist_items.count_items import count_items
from src.application.use_cases.waitlist_items.create_item import create_item
from src.config.tg_api import tg_api_settings
from src.domain.messages import waitlist_items_messages
from src.utils.parse_start_command_args import parse_start_command_args

router = Router()


@router.message(filters.CommandStart)
async def start_handler(message: types.Message):
    logging.info(f'Start: {message.from_user.id} {message.from_user.full_name} {time.asctime()}. Message: {message}')

    args = parse_start_command_args(message.text)
    uow = IUnitOfWork()

    if message.from_user.id in tg_api_settings.ADMIN_IDS:
        count = await count_items(uow)
        await message.reply(
            **waitlist_items_messages.waitlist_items_count(message, count=count).as_kwargs()
        )
    else:
        try:
            item_id = await create_item(
                uow,
                tg_id=message.from_user.id,
                utm_source=args.get('utm_source', 'undefined'),
                user_full_name=message.from_user.full_name
            )
        except ValueError:
            try:
                await message.reply(
                    **waitlist_items_messages.already_in_waitlist(message).as_kwargs()
                )
            except TelegramAPIError as e:
                logging.error(f"TelegramBadRequest: {e}")
            return
        try:

            await message.reply(
                **waitlist_items_messages.succesfully_joined_waitlist(message, item_id=item_id).as_kwargs()
            )
        except TelegramAPIError as e:
            logging.error(f"TelegramBadRequest: {e}")
