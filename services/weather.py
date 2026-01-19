import aiohttp
from config import OPENWEATHER_API_KEY


async def get_temperature(city: str) -> float:
    """Получить температуру по городу"""
    if not OPENWEATHER_API_KEY:
        return 20.0

    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["main"]["temp"]
                else:
                    return 20.0
    except:
        return 20.0