import os
from langchain_groq import ChatGroq
from app.services.tools import get_weather, get_clothing_advice
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"),model="openai/gpt-oss-20b",temperature=0.3)


def get_advice(city: str, thermo_offset = 0.0) -> dict:
    weather = get_weather(city)
    base_advice = get_clothing_advice(weather["feels_like"], thermo_offset)
    my_prompt = f"""Погода в {city}: реальная температура {weather["temp"]}°C, 
    ощущается как {weather["feels_like"]}°C, {weather["description"]}.
    Базовый совет: {base_advice}

    Напиши 2-3 предложения что надеть. Упомяни реальную и ощущаемую температуру. 
    Без эмодзи, без markdown."""
    response = llm.invoke(my_prompt)
    return {"city": city,
            "temp": weather["feels_like"],
            "description": weather["description"],
            "advice": response.content}





