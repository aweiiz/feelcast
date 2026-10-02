import secrets
from datetime import datetime, timezone, timedelta
import os
from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User, EmailToken

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"


class EmailRequest(BaseModel):
    email: str


class VerifyRequest(BaseModel):
    email: str
    code: str


@router.post("/request-code")
def request_code(data: EmailRequest, db: Session = Depends(get_db)):
    # Генерируем 6-значный код
    code = str(secrets.randbelow(900000) + 100000)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    # Инвалидируем старые коды для этого email
    db.query(EmailToken).filter(
        EmailToken.email == data.email,
        EmailToken.used == False
    ).update({"used": True})

    token = EmailToken(email=data.email, code=code, expires_at=expires_at)
    db.add(token)
    db.commit()

    # TODO: отправить на email, пока возвращаем в ответе для разработки
    return {"status": "ok", "debug_code": code}


@router.post("/verify-code")
def verify_code(data: VerifyRequest, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)

    token = db.query(EmailToken).filter(
        EmailToken.email == data.email,
        EmailToken.code == data.code,
        EmailToken.used == False,
        EmailToken.expires_at > now
    ).first()

    if not token:
        raise HTTPException(status_code=400, detail="Неверный или истёкший код")

    token.used = True

    # Находим или создаём пользователя
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        user = User(device_id=f"email:{data.email}", email=data.email)
        db.add(user)

    db.commit()
    db.refresh(user)

    # Выдаём JWT
    payload = {"sub": str(user.id), "email": user.email}
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}