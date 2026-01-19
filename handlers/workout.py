from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from services.calculations import calculate_workout_calories, calculate_water_for_workout
from database import get_user, save_user

router = Router()


@router.message(Command("log_workout"))
async def log_workout(message: Message):
    """Записать тренировку"""
    try:
        args = message.text.split()
        if len(args) < 3:
            await message.answer("Используйте: /log_workout <тип> <минуты>\nПример: /log_workout бег 15")
            return

        workout_type = args[1]
        minutes = float(args[2])

        user = get_user(message.from_user.id)
        if not user:
            await message.answer("Сначала настройте профиль: /set_profile")
            return

        calories_burned = calculate_workout_calories(
            workout_type = workout_type,
            duration_minutes = minutes,
            weight = user['weight']
        )

        water_bonus = calculate_water_for_workout(minutes)
        user['water_goal'] = user.get('water_goal', 0) + water_bonus
        user['burned_calories'] = user.get('burned_calories', 0) + calories_burned

        save_user(message.from_user.id, user)

        response = f"""
Тренировка записана: {workout_type} {minutes} минут

Результат:
• Сожжено: {calories_burned} ккал
• Всего сожжено сегодня: {user['burned_calories']} ккал
• Норма воды увеличена на: {water_bonus} мл
• Теперь нужно выпить: {user['water_goal']} мл за день
"""
        await message.answer(response)

    except ValueError:
        await message.answer("Ошибка формата! Используйте: /log_workout <тип> <минуты>")
    except KeyError:
        await message.answer("Ошибка: у пользователя нет веса. Сначала /set_profile")