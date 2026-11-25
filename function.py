from sqlalchemy import Integer, String, Date, Column, create_engine, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, date, timedelta, timezone
import jwt
from argon2 import PasswordHasher
from fastapi import HTTPException
from pydantic import BaseModel, Field
ph = PasswordHasher()

DB_PATH = "campus.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7*24*60
ALGORITHM = "HS256"

class Register(BaseModel):
    username: str = Field(min_length=1)
    email: str = Field
    password: str = Field(min_length=4)
    
class AttendanceIn(BaseModel):
    student_id: int

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)
    created_at = Column(String)

class Club(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    category = Column(String)
    coordinator_id = Column(Integer, ForeignKey("users.user_id"))

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey("clubs.id"))
    title = Column(String)
    description = Column(String)
    venue = Column(String)
    date = Column(Date)
    capacity = Column(Integer)
    registration_deadline = Column(Date)

Base.metadata.create_all(engine)
