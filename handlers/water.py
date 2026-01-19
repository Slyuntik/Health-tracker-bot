from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database import get_user, save_user

router = Router()


@router.message(Command("log_water"))
async def log_water(message: Message):
    """Записать выпитую воду"""
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.answer("Используйте: /log_water <количество в мл>")
            return

        amount = float(args[1])

        user = get_user(message.from_user.id)
        if not user:
            await message.answer("Сначала настройте профиль: /set_profile")
            return

        user['logged_water'] = user.get('logged_water', 0) + amount
        save_user(message.from_user.id, user)

        remaining = max(0, user['water_goal'] - user['logged_water'])

        response = f"""
Вода записана: +{amount} мл

Прогресс:
Выпито: {user['logged_water']}/{user['water_goal']} мл
Осталось: {remaining} мл
"""
        await message.answer(response)

    except ValueError:
        await message.answer("Введите число! Например: /log_water 500")