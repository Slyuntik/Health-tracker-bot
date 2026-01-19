from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database import get_user

router = Router()


@router.message(Command("check_progress"))
async def check_progress(message: Message):
    """Показать текущий прогресс"""
    user = get_user(message.from_user.id)
    if not user:
        await message.answer("Сначала настройте профиль: /set_profile")
        return

    calorie_balance = user.get('logged_calories', 0) - user.get('burned_calories', 0)
    calories_left = max(0, user.get('calorie_goal', 0) - calorie_balance)
    water_left = max(0, user.get('water_goal', 0) - user.get('logged_water', 0))

    response = f"""
Прогресс за сегодня:

ВОДА:
• Выпито: {user.get('logged_water', 0)}/{user.get('water_goal', 0)} мл
• Осталось: {water_left} мл

КАЛОРИИ:
• Потреблено: {user.get('logged_calories', 0):.1f} ккал
• Сожжено: {user.get('burned_calories', 0):.1f} ккал
• Баланс: {calorie_balance:.1f} ккал
• До цели: {calories_left:.1f} ккал
"""
    await message.answer(response)