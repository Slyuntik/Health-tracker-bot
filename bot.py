import asyncio
import logging
import sys
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import router

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/tmp/bot.log", encoding = "utf-8")
    ]
)
logger = logging.getLogger(__name__)


async def main():
    if not BOT_TOKEN:
        logger.error("Токен бота не найден! Укажите BOT_TOKEN")
        return

    bot = Bot(token = BOT_TOKEN)
    dp = Dispatcher(storage = MemoryStorage())
    dp.include_router(router)

    @dp.update.outer_middleware()
    async def log_middleware(handler, event, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if event.message and event.message.from_user:
            user = event.message.from_user
            user_id = user.id
            username = user.username or user.first_name
            command = event.message.text or "медиа-сообщение"

            logger.info(f"[{timestamp}] Команда от @{username} (ID: {user_id}): {command}")

        try:
            result = await handler(event, data)
            return result
        except Exception as e:
            logger.error(f"[{timestamp}] Ошибка: {e}")
            raise

    bot_info = await bot.get_me()
    logger.info(f"Бот запущен: @{bot_info.username}")
    logger.info(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        await dp.start_polling(bot, allowed_updates = dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Бот упал: {e}")
        raise
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logger.info("Запуск бота...")
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("Бот остановлен пользователем")
            break
        except Exception as e:
            logger.error(f"Перезапуск из-за ошибки: {e}")
            import time

            time.sleep(5)