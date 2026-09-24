from datetime import timezone, datetime

from fastapi import FastAPI, Depends, HTTPException
from app.api.auth import get_current_user
from app.db.models import User, Review
from app.services.advisor import get_advice
from app.services.profile import get_or_create_profile
from app.schemas.onboarding import OnboardingRequest, CheckinRequest
from app.db.database import get_db
from sqlalchemy.orm import Session
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()


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
    db: Session = Depends(get_db),
):
    offset_map = {"мёрзну больше": -3.0, "нормально": 0.0, "жарко чаще": 3.0}
    profile = get_or_create_profile(user.id, db)
    answers_json = json.dumps(
        {
            "cold_sensitivity": data.cold_sensitivity.value,
            "climate": data.climate.value,
            "activity": data.activity.value,
            "rain_sensitivity": data.rain_sensitivity.value,
            "gender": data.gender,
        }
    )
    profile.base_answers = answers_json
    profile.thermo_offset = offset_map.get(data.cold_sensitivity.value, 0.0)

    db.commit()
    return {"status": "ok", "user_id": user.id}


@app.post("/advice/{city}")
async def advice(
    city: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    reviews = (
        db.query(Review)
        .filter(Review.city == city)
        .order_by(Review.created_at.desc())
        .limit(20)
        .all()
    )
    profile = get_or_create_profile(user.id, db)
    return get_advice(city, profile.thermo_offset, reviews)


@app.post("/checkin")
async def checkin(
    data: CheckinRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_or_create_profile(user.id, db)
    profile.thermo_offset += data.intensity * 0.5
    review = Review(
        user_id=user.id,
        city=data.city,
        feeling=str(data.intensity),
        comment=data.comment,
        created_at=datetime.now(timezone.utc),
    )
    db.add(review)
    db.commit()
    return {"status": "ok", "thermo_offset": profile.thermo_offset}


@app.get("/feed")
async def feed(city: str, db: Session = Depends(get_db)):
    reviews = (
        db.query(Review)
        .filter(Review.city == city)
        .order_by(Review.created_at.desc())
        .limit(20)
        .all()
    )
    return [
        {"intensity": r.feeling, "comment": r.comment, "created_at": r.created_at}
        for r in reviews
    ]
