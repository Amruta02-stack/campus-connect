from sqlalchemy import create_engine
from sqlalchemy.orm import Session,declarative_base
from fastapi import HTTPException
from datetime import datetime,timedelta,timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel,Field,EmailStr
from AM_functions import Users, Club


ph=PasswordHasher()

DB_PATH = "campus.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


ACCEESS_TOKEN_EXPIRY=120
REFRESH_TOKEN_EXPIRY=7*24*60
SECRET_KEY="SECRET321"
ALGORITHM="HS256"


class CoordinatorRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

def create_token(username, user_type, token_type):
    time = ACCEESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload = {
        "username": username,
        "token_type": token_type,
        "user_type": user_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time)
    }
    token = jwt.encode(payload=payload,key=SECRET_KEY,algorithm=ALGORITHM)
    return token


def verify_token(token, token_type):
    if not token:
        return False
    try:
        payload = jwt.decode(jwt=token,key=SECRET_KEY,algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return False
    if payload.get("token_type") == token_type:
        return payload
    return False

def create_admin():
    session = Session(engine)
    existing_admin = session.query(Users).filter_by( email="admin@gmail.com").first()
    if not existing_admin:
        admin = Users(username="admin",email="admin@gmail.com",password=ph.hash("admin12345"),role="admin")
        session.add(admin)
        session.commit()
    session.close()