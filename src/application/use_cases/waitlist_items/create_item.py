from src.application.uow.uow import IUnitOfWork


async def create_item(
    uow: IUnitOfWork,
    tg_id: int,
    utm_source: str,
    user_full_name: str | None,
) -> int:
    async with uow:
        if await uow.waitlist_items.get_by_tg_id(tg_id=tg_id) is not None:
            raise ValueError("User already in waitlist")
        item_id = await uow.waitlist_items.create(
            tg_id=tg_id,
            utm_source=utm_source,
            user_full_name=user_full_name
        )
        await uow.commit()
    return item_id
