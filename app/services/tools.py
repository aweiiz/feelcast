from dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_weather(city: str) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather"

    response = requests.get(url, params={"q": city, "appid": api_key, "units": "metric"})
    data = response.json()

    return {
        "city": city,
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "wind_speed": data["wind"]["speed"],
        "precipitation": data.get("rain", {}).get("1h", 0),
        "description": data["weather"][0]["description"]
    }


def get_clothing_advice(feels_like: float, thermo_offset: float = 0.0) -> str:
    adjusted = feels_like + thermo_offset
    if adjusted < 0:
        return "Очень холодно. Тёплая куртка, шапка, перчатки обязательны."
    elif adjusted < 10:
        return "Холодно. Куртка, свитер, закрытая обувь."
    elif adjusted < 18:
        return "Прохладно. Лёгкая куртка или толстовка."
    elif adjusted < 25:
        return "Комфортно. Футболка, джинсы."
    else:
        return "Жарко. Лёгкая одежда, не забудь воду."
#    return f'Температура ощущается как {feels_like}, поэтому рекомендуем надеть '


