from __future__ import annotations
from typing import TYPE_CHECKING
from typing import NoReturn
import logging

from aiogram import Bot

from src.config.server import server_settings
from src.domain.repositories.waitlist_items import WaitlistItemsRepository
from src.infrastructure.database.base import async_session_maker

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class IUnitOfWork:
    bot: Bot
    waitlist_items: WaitlistItemsRepository

    def init_repositories(self, session: AsyncSession) -> None:
        self.waitlist_items = WaitlistItemsRepository(session)

    def __init__(self) -> None:
        self.session_factory = async_session_maker

        self.logger = logging.getLogger(__name__)

        self._session = None
        self._session_nesting_level = 0

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("An attempt to access the session was unsuccessful. Maybe you forgot to initialize it "
                               "via __aenter__ (async with uow)")
        return self._session

    @session.setter
    def session(self, value: AsyncSession) -> None:
        self._session = value

    async def __aenter__(self) -> None:
        self._session_nesting_level += 1
        if self._session_nesting_level == 1:  # if session is not initialized
            self._session = self.session_factory()
            self.init_repositories(self._session)

    async def __aexit__(self, *args: object) -> None:
        if self._session_nesting_level == 1 and self._session is not None:  # if session is initialized
            await self.rollback()
        self._session_nesting_level -= 1

    async def commit(self) -> None:
        if self._session_nesting_level == 1:
            await self.session.commit()
            await self.session.close()
            self.session = None

    async def rollback(self) -> None:
        if self._session_nesting_level == 1:
            await self.session.rollback()
            await self.session.close()
            self.session = None

    def __getattr__(self, item):
        raise AttributeError(f"Attribute {item} not found. If you want to access the repository, "
                             f"you need to initialize it via __aenter__ (async with uow)")
