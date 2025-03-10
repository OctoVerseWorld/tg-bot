import datetime

from sqlalchemy import func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.metadata import Base


class WaitlistItemModel(Base):
    __tablename__ = 'waitlist_items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True, index=True)
    utm_source: Mapped[str]
    user_full_name: Mapped[str | None]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
