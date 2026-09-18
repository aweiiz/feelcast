from fastapi import FastAPI, Depends, HTTPException
from app.auth import get_current_user
from app.models import User, init_db, Profile
from app.advisor import get_advice
from app.schemas import OnboardingRequest
from app.database import get_db
from sqlalchemy.orm import Session
import json
app = FastAPI()
init_db()

@app.get("/weather/{city}")
async def weather(city: str):
    result = get_advice(city)
    return result


@app.get("/whoami")
async def whoami(user: User = Depends(get_current_user)):
    return {"user_id": user.id, "device_id": user.device_id}

@app.post("/onboarding")
async def onboarding(
    data: OnboardingRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    answers_json = json.dumps(
        {"cold_sensitivity": data.cold_sensitivity.value,
    "climate": data.climate.value,
    "activity": data.activity.value,
    "rain_sensitivity": data.rain_sensitivity.value,
    "gender": data.gender}
    )

    if profile is None:
        profile = Profile(
            user_id=user.id,
            base_answers=answers_json,
            thermo_offset=0.0
        )
        db.add(profile)
    else:
        profile.base_answers = answers_json  # обновляем

    db.commit()
    return {"status": "ok", "user_id": user.id}




