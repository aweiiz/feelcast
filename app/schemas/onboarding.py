from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ColdSensitivity(str, Enum):
    freezes_more = "мёрзну больше"
    normal = "нормально"
    hot_more = "жарко чаще"


class Climate(str, Enum):
    warm = "тёплый"
    moderate = "умеренный"
    cold = "холодный"


class Activity(str, Enum):
    low = "мало хожу"
    normal = "обычная ходьба"
    active = "активно"
    sport = "спорт"

class RainSensitivity(str, Enum):
    not_important = "не важно"
    somewhat = "немного важно"
    very_important = "очень важно"



class OnboardingRequest(BaseModel):
    cold_sensitivity: ColdSensitivity
    climate: Climate
    activity: Activity
    rain_sensitivity: RainSensitivity
    gender: Optional[str] = None

class CheckinRequest(BaseModel):
    city: str
    intensity: int = Field(..., ge=-2, le=2)  # от -2 до +2
    comment: Optional[str] = None