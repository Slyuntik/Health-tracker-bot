from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для отслеживания норм воды и калорий.\n\n"
        "Основные команды:\n"
        "/set_profile - настроить профиль (обязательно!)\n"
        "/log_water <мл> - записать воду\n"
        "/log_food <продукт> - записать еду\n"
        "/log_workout <тип> <минуты> - записать тренировку\n"
        "/check_progress - проверить прогресс\n"
        "/help - помощь"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Помощь:\n\n"
        "1. Настройте профиль: /set_profile\n"
        "2. Записывайте воду: /log_water 500\n"
        "3. Записывайте еду: /log_food яблоко\n"
        "4. Записывайте тренировки: /log_workout бег 15\n"
        "5. Проверяйте прогресс: /check_progress"
    )