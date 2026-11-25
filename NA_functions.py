from sqlalchemy import create_engine,Integer,String,Date,Column,ForeignKey,Boolean
from sqlalchemy.orm import Session,declarative_base
from fastapi import FastAPI,HTTPException
from datetime import date,datetime,timedelta,timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel,Field,EmailStr
from typing import Optional 
import AM_functions as a
from AM_functions import Users


ph=PasswordHasher()
DB_PATH = "campus.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

ACCEESS_TOKEN_EXPIRY=120
REFRESH_TOKEN_EXPIRY=7*24*60

ALGORITHM="HS256"

class RegisterIn(BaseModel):
    username: str
    email: EmailStr
    password: str

# def register_user(username: str, email: str, password: str):
#     email = email.lower()
#     with Session(engine) as session:
#         if session.query(a.Users).filter_by(email=email).first():
#             return None
#         user = a.Users(
#             username=username,
#             email=email,
#             password=ph.hash(password),
#             role="student", 
#         )
#         session.add(user)
#         session.commit()
#         session.refresh(user)
#         return {"id": user.id, "username": user.username,
#                 "email": user.email, "role": user.role}


def registar_user(username: str, email: str, password: str):
    email = email.lower()

    with Session(engine) as session:
        existing_user = session.query(Users).filter_by(email=email).first()

        if existing_user:
            return None

        hashed_password = ph.hash(password)

        user = Users(
            username=username,
            email=email,
            password=hashed_password,
            role="student"
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }