from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.calculations import calculate_water_goal, calculate_calorie_goal
from services.weather import get_temperature
from database import save_user


router = Router()


class ProfileStates(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity = State()
    city = State()


@router.message(Command("set_profile"))
async def start_profile(message: Message, state: FSMContext):
    await message.answer("Настройка профиля. Введите ваш вес (кг):")
    await state.set_state(ProfileStates.weight)


@router.message(ProfileStates.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text)
        await state.update_data(weight = weight)
        await message.answer("Введите ваш рост (см):")
        await state.set_state(ProfileStates.height)
    except:
        await message.answer("Введите число!")


@router.message(ProfileStates.height)
async def process_height(message: Message, state: FSMContext):
    try:
        height = float(message.text)
        await state.update_data(height = height)
        await message.answer("Введите ваш возраст:")
        await state.set_state(ProfileStates.age)
    except:
        await message.answer("Введите число!")


@router.message(ProfileStates.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age = age)
        await message.answer("Сколько минут активности в день? (например: 60):")
        await state.set_state(ProfileStates.activity)
    except:
        await message.answer("Введите целое число!")


@router.message(ProfileStates.activity)
async def process_activity(message: Message, state: FSMContext):
    try:
        activity = float(message.text)
        await state.update_data(activity = activity)
        await message.answer("В каком городе вы находитесь? (например: Moscow):")
        await state.set_state(ProfileStates.city)
    except:
        await message.answer("Введите число!")


@router.message(ProfileStates.city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()
    data = await state.get_data()

    try:
        temp = await get_temperature(city)
    except:
        temp = 20

    water_goal = calculate_water_goal(
        weight = data['weight'],
        activity_minutes = data['activity'],
        temperature = temp
    )

    calorie_goal = calculate_calorie_goal(
        weight = data['weight'],
        height = data['height'],
        age = data['age']
    )

    user_data = {
        **data,
        'city': city,
        'water_goal': water_goal,
        'calorie_goal': calorie_goal,
        'logged_water': 0,
        'logged_calories': 0,
        'burned_calories': 0
    }

    save_user(message.from_user.id, user_data)

    response = f"""
Профиль сохранен!

Ваши нормы:
• Вода: {water_goal} мл/день
• Калории: {calorie_goal} ккал/день
• Город: {city} ({temp}°C)

Используйте:
/log_water <мл> - записать воду
/log_food <продукт> - записать еду
/log_workout <тип> <минуты> - записать тренировку
/check_progress - проверить прогресс
"""

    await message.answer(response)
    await state.clear()