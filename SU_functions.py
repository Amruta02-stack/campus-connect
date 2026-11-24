from sqlalchemy import Integer,String ,Column, ForeignKey, create_engine ,Date
from sqlalchemy.orm import Session, declarative_base 
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError 
from datetime import date, datetime, timedelta, timezone


ph = PasswordHasher()

ACCESS_TOKEN_EXPIRY = 120
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
ALGORITHM = "HS256"

DB_PATH = "sqlite:///./campus_connect.db"
engine = create_engine(DB_PATH)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    created_at = Column(Date, default=date.today)


class Club(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    coordinator_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date, default=date.today())

Base.metadata.create_all(engine)



