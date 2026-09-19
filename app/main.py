from fastapi import FastAPI, Depends, HTTPException
from app.api.auth import get_current_user
from app.db.models import User, init_db, Profile
from app.services.advisor import get_advice
from app.schemas.onboarding import OnboardingRequest
from app.db.database import get_db
from sqlalchemy.orm import Session
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
app = FastAPI()
init_db()


app.mount("/static", StaticFiles(directory="app/static"), name="static")
@app.get("/")
async def root():
    return FileResponse("app/static/index.html")


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
    offset_map = {
        "мёрзну больше": -3.0,
        "нормально": 0.0,
        "жарко чаще": 3.0
    }
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    answers_json = json.dumps(
        {"cold_sensitivity": data.cold_sensitivity.value,
    "climate": data.climate.value,
    "activity": data.activity.value,
    "rain_sensitivity": data.rain_sensitivity.value,
    "gender": data.gender}
    )
    thermo_offset = offset_map.get(data.cold_sensitivity.value, 0.0)
    if profile is None:
        profile = Profile(
            user_id=user.id,
            base_answers=answers_json,
            thermo_offset=thermo_offset
        )
        db.add(profile)
    else:
        profile.base_answers = answers_json # обновляем
        profile.thermo_offset = thermo_offset

    db.commit()
    return {"status": "ok", "user_id": user.id}

@app.post("/advice/{city}")
async def advice(city: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        profile = db.query(Profile).filter(Profile.user_id == user.id).first()
        thermo_offset = profile.thermo_offset if profile else 0.0
        return get_advice(city, thermo_offset)


