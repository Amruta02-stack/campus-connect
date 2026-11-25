from sqlalchemy import create_engine,Integer,String,Date,Column,ForeignKey,Boolean
from sqlalchemy.orm import Session,declarative_base
from fastapi import FastAPI,HTTPException
from datetime import date,datetime,timedelta,timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel,Field,EmailStr
from typing import Optional   

import SU_functions as s

ph=PasswordHasher()

DB_PATH = "campus.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


ACCEESS_TOKEN_EXPIRY=120
REFRESH_TOKEN_EXPIRY=7*24*60
SECRET_KEY="SECRET321"
ALGORITHM="HS256"

class LoginIn(BaseModel):
    email:EmailStr
    password:str = Field(min_length=8)

class UserIn(BaseModel):  
    username:str= Field(min_length=1)
    email:EmailStr
    password:str = Field(min_length=8)  

class ClubIn(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    category: str = Field(min_length=1)
    coordinator_id: int

class ClubUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class EventIn(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    venue: str = Field(min_length=1)
    date: date
    regis_deadline: date
    max_cap: int = Field(gt=0)



class Users(Base):
    __tablename__="Users"

    id=Column(Integer,primary_key=True)
    username=Column(String)
    role=Column(String,default="student")
    email=Column(String)
    password=Column(String)

class Club(Base):
    __tablename__ = "Clubs"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    coordinator_id = Column(Integer, ForeignKey("Users.id"))
   

class Club_members(Base):
    __tablename__ = "Clubs_members"

    id=Column(Integer,primary_key=True)
    club_id=Column(Integer,ForeignKey("Clubs.id"))
    stu_id=Column(Integer,ForeignKey("Users.id"))
    status=Column(String,default="pending")

class Events(Base):
    __tablename__ = "Events"

    id=Column(Integer,primary_key=True)
    club_id=Column(Integer,ForeignKey("Clubs.id"))
    title=Column(String)
    description=Column(String)
    venue=Column(String)
    date=Column(Date)
    regis_deadline=Column(Date)
    max_cap=Column(Integer)


class Event_regis(Base):
    __tablename__ = "Event_regis"

    id = Column(Integer,primary_key=True)
    event_id=Column(Integer,ForeignKey("Events.id"))
    stu_id=Column(Integer,ForeignKey("Users.id"))
    status=Column(String,default="registered")
    attended=Column(Boolean,default=False)

Base.metadata.create_all(engine)
                             

# def verify_login(email,password):
#     session=Session(engine)
#     user=session.query(Users).filter_by(email=email).first()
#     if user is None:
#         session.close()
#         return False
#     try:
#         ph.verify(user.password,password)
#     except VerifyMismatchError:
#         session.close()
#         return False
    
#     access_token=s.create_token(username=username,user_type=user.role,token_type="access")
#     refresh_token=s.create_token(username=username,user_type=user.role,token_type="refresh")
#     session.close()
#     return {"access_token":access_token,"refresh_token":refresh_token}

def verify_login(email, password):
    session = Session(engine)
    email = email.lower()
    user = session.query(Users).filter_by(email=email).first()
    if user is None:
        print("USER NOT FOUND")
        session.close()
        return False
    try:
        ph.verify(user.password, password)
        print("PASSWORD MATCHED")
    except VerifyMismatchError:
        print("WRONG PASSWORD")
        session.close()
        return False
    access_token = s.create_token(username=user.username, user_type=user.role, token_type="access")
    refresh_token = s.create_token(username=user.username, user_type=user.role, token_type="refresh")
    session.close()
    return {"access_token": access_token,"refresh_token": refresh_token}
