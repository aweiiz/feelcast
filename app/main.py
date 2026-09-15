from fastapi import FastAPI, Depends, HTTPException
from app.auth import get_current_user
from app.models import User, init_db
from app.advisor import get_advice
app = FastAPI()
init_db()

@app.get("/weather/{city}")
async def weather(city: str):
    result = get_advice(city)
    return result


@app.get("/whoami")
async def whoami(user: User = Depends(get_current_user)):
    return {"user_id": user.id, "device_id": user.device_id}
