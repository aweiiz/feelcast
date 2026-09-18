from pydantic import BaseModel
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

