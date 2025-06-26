from aiogram import Router
from aiogram.filters import Command

from .start import start_cmd


def User_handler_router() -> Router:
    router = Router()

    router.message(Command("start"))(start_cmd)

    return router
