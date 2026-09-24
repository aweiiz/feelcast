from app.db.models import User
from app.db.database import get_db, SessionLocal
from fastapi import Depends, Header


def get_current_user(
    x_device_id: str = Header(..., alias="X-Device-ID"),
    db: SessionLocal = Depends(get_db),
) -> User:
    user = db.query(User).filter(User.device_id == x_device_id).first()
    if user is None:
        user = User(device_id=x_device_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
