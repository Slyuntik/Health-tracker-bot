def calculate_water_goal(weight, activity_minutes, temperature=20):
    """Формула из задания"""
    base = weight * 30
    activity_bonus = (activity_minutes / 30) * 500
    weather_bonus = 500 if temperature > 25 else 0

    total = base + activity_bonus + weather_bonus

    return round(total)


def calculate_calorie_goal(weight, height, age):
    """Формула из задания"""
    base = 10 * weight + 6.25 * height - 5 * age

    return round(base)


def calculate_workout_calories(workout_type, duration_minutes, weight):
    """
    Рассчитать сожжённые калории за тренировку
    """
    coefficients = {
        'ходьба': 3,
        'бег': 8,
        'велосипед': 7,
        'плавание': 6,
        'футбол': 7,
        'теннис': 8,
        'баскетбол': 6,
        'тренажеры': 5,
    }

    workout_lower = workout_type.lower()
    coeff = 5

    for key, value in coefficients.items():
        if key in workout_lower:
            coeff = value
            break

    calories = coeff * weight * (duration_minutes / 60)
    return round(calories)


def calculate_water_for_workout(duration_minutes):
    """
    Рассчитать дополнительную потребность в воде для тренировки
    """
    return round((duration_minutes / 30) * 200)