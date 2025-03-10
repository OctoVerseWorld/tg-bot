from src.application.uow.uow import IUnitOfWork


async def count_items(
    uow: IUnitOfWork,
) -> int:
    async with uow:
        count = await uow.waitlist_items.count()
        await uow.commit()
    return count
