import asyncio
import colorlog
import logging

from aiogram import Bot, Dispatcher, Router

from Bot.config import settings
from Bot.Handlers import Handler_Router
from Bot.Callbacks import Callback_Router


class TelegramBot:
    def __init__(self, token: str, log_level: int = logging.INFO):
        self._setup_logging(log_level)
        self.logger = logging.getLogger(__name__)

        self.logger.info("Инициализация бота...")
        self.bot = Bot(token=token)
        self.dp = Dispatcher()

        self._setup_middleware()
        self._setup_routers(Handler_Router(), Callback_Router())
        self.logger.info("Бот инициализирован")

    def _setup_logging(self, level: int):
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            )
        )

        logging.basicConfig(level=level, handlers=[handler])
        logging.getLogger("aiogram").setLevel(logging.WARNING)
        logging.getLogger("asyncio").setLevel(logging.WARNING)

    def _setup_routers(self, *routers: Router):
        """Добавление роутеров"""
        self.logger.debug(f"Добавление {len(routers)} роутеров...")
        for router in routers:
            self.dp.include_router(router=router)
        self.logger.debug("Роутеры добавлены")

    def _setup_middleware(self):
        """Настройка middleware"""
        self.logger.debug("Настройка middleware...")
        # self.dp.message.middleware(YourMiddleware())
        self.logger.debug("Middleware настроены")

    async def run(self):
        """Запуск бота с обработкой ошибок"""
        self.logger.info("Запуск бота...")
        try:
            await self.dp.start_polling(self.bot)
        except Exception as e:
            self.logger.critical(f"Ошибка при работе бота: {e}", exc_info=True)
            raise
        finally:
            self.logger.info("Бот остановлен")
            await self.bot.session.close()


if __name__ == "__main__":
    bot = TelegramBot(settings.TOKEN, log_level=logging.INFO)
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("Бот остановлен по запросу пользователя")
