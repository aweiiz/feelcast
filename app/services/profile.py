from sqlalchemy.orm import Session
from app.db.models import Profile


def get_or_create_profile(user_id: int, db: Session) -> Profile:
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile is None:
        profile = Profile(user_id=user_id, thermo_offset=0.0)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile
