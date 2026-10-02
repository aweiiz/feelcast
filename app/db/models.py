from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
    Boolean
)
from sqlalchemy.orm import relationship
from app.db.database import Base, engine
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    device_id = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    nickname = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    profile = relationship("Profile", back_populates="user", uselist=False)


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cold_sensitivity = Column(String)
    climate = Column(String)
    activity_level = Column(Integer)
    base_answers = Column(String)  # добавь
    thermo_offset = Column(Float, default=0.0)
    user = relationship("User", back_populates="profile")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String)
    temperature = Column(Float)
    feeling = Column(String)
    clothing = Column(String)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class EmailToken(Base):
    __tablename__ = "email_tokens"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    code = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)



def init_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
