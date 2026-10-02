from app.db.models import User
from app.db.database import get_db, SessionLocal
from fastapi import Depends, Header, HTTPException
from jose import jwt, JWTError
from typing import Optional
import os

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"


def get_current_user(
    x_device_id: Optional[str] = Header(None, alias="X-Device-ID"),
    authorization: Optional[str] = Header(None),
    db: SessionLocal = Depends(get_db),
) -> User:

    # Вариант 1 — JWT токен в заголовке Authorization: Bearer <token>
    if authorization and authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = int(payload["sub"])
        except (JWTError, KeyError, ValueError):
            raise HTTPException(status_code=401, detail="Невалидный токен")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        return user

    # Вариант 2 — старый device_id (гостевой режим)
    if x_device_id:
        user = db.query(User).filter(User.device_id == x_device_id).first()
        if user is None:
            user = User(device_id=x_device_id)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    raise HTTPException(status_code=401, detail="Нужен X-Device-ID или Authorization")