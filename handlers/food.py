from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.food_api import find_product
from database import get_user, save_user

router = Router()


class FoodStates(StatesGroup):
    waiting_for_amount = State()


@router.message(Command("log_food"))
async def log_food_start(message: Message, state: FSMContext):
    """Начать запись еды"""
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Используйте: /log_food <название продукта>")
        return

    product_name = " ".join(args[1:])
    product = await find_product(product_name)

    await state.update_data(
        product = product,
        product_name = product_name
    )

    await message.answer(
        f"{product['name']} — {product['calories']} ккал на 100г\n"
        f"Сколько грамм вы съели?"
    )
    await state.set_state(FoodStates.waiting_for_amount)


@router.message(FoodStates.waiting_for_amount)
async def log_food_amount(message: Message, state: FSMContext):
    """Обработать количество еды"""
    try:
        grams = float(message.text)
        data = await state.get_data()

        calories = (grams / 100) * data['product']['calories']

        user = get_user(message.from_user.id)
        if user:
            user['logged_calories'] = user.get('logged_calories', 0) + calories
            save_user(message.from_user.id, user)

            response = f"""
Записано: {data['product']['name']} ({grams}г)
Калории: {calories:.1f} ккал
Всего сегодня: {user['logged_calories']:.1f} ккал
"""
            await message.answer(response)
        else:
            await message.answer("Ошибка: профиль не найден. Сначала /set_profile")

        await state.clear()

    except ValueError:
        await message.answer("Введите число грамм!")