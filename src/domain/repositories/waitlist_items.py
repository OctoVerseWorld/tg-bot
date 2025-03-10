import datetime

from sqlalchemy import insert, select, func

from src.domain.models.waitlist_items import WaitlistItemModel
from src.domain.repositories.abstract import AbstractRepository


class WaitlistItemsRepository(AbstractRepository):
    async def create(self, tg_id: int, utm_source: str, user_full_name: str) -> int:
        stmt = (
            insert(
                WaitlistItemModel
            ).values(
                tg_id=tg_id,
                utm_source=utm_source,
                user_full_name=user_full_name,
            ).returning(
                WaitlistItemModel.id
            )
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def count(self) -> int:
        stmt = (
            select(func.count(WaitlistItemModel.id))
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def get_by_tg_id(self, tg_id: int) -> int | None:
        stmt = (
            select(
                WaitlistItemModel.id
            )
            .where(
                WaitlistItemModel.tg_id == tg_id
            )
        )
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()
