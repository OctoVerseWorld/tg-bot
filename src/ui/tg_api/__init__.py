from aiogram import Router


from .commands.start import router as commands_start_router


router = Router()


router.include_router(commands_start_router)
