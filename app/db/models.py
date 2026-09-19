from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
from app.db.database import Base, engine


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
    created_at = Column(DateTime)


def init_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()


