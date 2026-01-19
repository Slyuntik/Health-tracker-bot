import aiohttp


async def find_product(product_name: str) -> dict:
    """Найти продукт в OpenFoodFacts и получить его калорийность"""
    url = f"https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 3
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params = params, timeout = 5) as response:
                if response.status == 200:
                    data = await response.json()
                    products = data.get('products', [])

                    if products:
                        for product in products:
                            calories = product.get('nutriments', {}).get('energy-kcal_100g')
                            if calories:
                                return {
                                    'name': product.get('product_name', product_name),
                                    'calories': calories,
                                    'brand': product.get('brands', ''),
                                    'quantity': product.get('quantity', '')
                                }

        return get_fallback_product(product_name)

    except Exception as e:
        print(f"Ошибка API OpenFoodFacts: {e}")
        return get_fallback_product(product_name)


def get_fallback_product(product_name: str) -> dict:
    """Готовая база продуктов, если API не сработает"""
    common_foods = {
        'банан': {'name': 'Банан', 'calories': 89},
        'яблоко': {'name': 'Яблоко', 'calories': 52},
        'яйцо': {'name': 'Яйцо куриное', 'calories': 155},
        'хлеб': {'name': 'Хлеб белый', 'calories': 265},
        'молоко': {'name': 'Молоко', 'calories': 42},
        'курица': {'name': 'Курица грудка', 'calories': 165},
        'рис': {'name': 'Рис вареный', 'calories': 130},
        'картофель': {'name': 'Картофель', 'calories': 77},
        'макароны': {'name': 'Макароны', 'calories': 131},
        'сыр': {'name': 'Сыр', 'calories': 402},
        'помидор': {'name': 'Помидор', 'calories': 18},
        'огурец': {'name': 'Огурец', 'calories': 15},
        'кофе': {'name': 'Кофе', 'calories': 0},
        'чай': {'name': 'Чай', 'calories': 1},
        'сахар': {'name': 'Сахар', 'calories': 387},
        'соль': {'name': 'Соль', 'calories': 0},
        'вода': {'name': 'Вода', 'calories': 0},
    }

    product_lower = product_name.lower()
    for key, value in common_foods.items():
        if key in product_lower:
            return value

    return {'name': product_name, 'calories': 150}