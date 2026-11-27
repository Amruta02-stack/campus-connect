from sqlalchemy import create_engine,Integer,String,Date,Column,ForeignKey,Boolean
from sqlalchemy.orm import Session,declarative_base
from fastapi import FastAPI,HTTPException
import os
from datetime import date,datetime,timedelta,timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel,Field,EmailStr
from typing import Optional   



ph=PasswordHasher()
DB_PATH = "campus.db"

engine = create_engine("sqlite:///./campus.db")
Base = declarative_base()


ACCEESS_TOKEN_EXPIRY=120
REFRESH_TOKEN_EXPIRY=7*24*60
ALGORITHM="HS256"
SECRET_KEY=os.getenv("SECRET_KEY")


class LoginIn(BaseModel):
    email:EmailStr
    password:str 

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
    event_date: date
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
    event_date=Column(Date)
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

import SU_functions as s

def verify_login(email,password):
    session=Session(engine)
    user=session.query(Users).filter_by(email=email).first()
    if user is None:
        session.close()
        return False
    try:
        ph.verify(user.password,password)
    except VerifyMismatchError:
        session.close()
        return False
    
    access_token=s.create_token(email=email,role=user.role,token_type="access")
    refresh_token=s.create_token(email=email,role=user.role,token_type="refresh")
    session.close()
    return {"access_token":access_token,"refresh_token":refresh_token}


def apply_club(club_id,payload):
    session=Session(engine)
    user=session.query(Users).filter_by(email=payload["email"]).first()
    if user is None:
        session.close()
        raise HTTPException(status_code=404,detail="Student Not Found")
    club=session.query(Club).filter_by(id=club_id).first()
    if club is None:
        session.close()
        raise HTTPException(status_code=404,detail="Club Not Found")

    memeber=session.query(Club_members).filter_by(club_id=club_id,stu_id=user.id).first()
    if memeber is not None:
        session.close()
        raise HTTPException(status_code=409, detail="You already applied to the club")
    session.add(Club_members(club_id=club_id,stu_id=user.id))
    session.commit()
    session.close()    
    return True

def decide_membership(status,payload,member_id,club_id):
    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=422,detail="Invaild status")
    session=Session(engine)
    user = session.query(Users).filter_by(email=payload["email"]).first()
    if user is None:
        session.close()
        raise HTTPException(status_code=404,detail="Student Not Found")
    club=session.query(Club).filter_by(id=club_id).first()
    if club is None:
        session.close()
        raise HTTPException(status_code=404,detail="Club Not Found")
    if club.coordinator_id !=user.id:
        session.close()
        raise  HTTPException(status_code=403,detail="You are not the club coordinator")
    memeber=session.query(Club_members).filter_by(id=member_id,club_id=club_id).first()
    if memeber is None:
        session.close()
        raise HTTPException(status_code=409, detail="student Not found")

    memeber.status=status
    session.commit()
    session.close()
    return True

def get_club_members(club_id,payload):
    session=Session(engine)
    user = session.query(Users).filter_by(email=payload["email"]).first()
    if user is None:
        session.close()
        raise HTTPException(status_code=404,detail="Student Not Found")
    club=session.query(Club).filter_by(id=club_id).first()
    if club is None:
        session.close()
        raise HTTPException(status_code=404,detail="Club Not Found")
    if club.coordinator_id !=user.id:
        session.close()
        raise  HTTPException(status_code=403,detail="You are not the club coordinator")
    members=session.query(Club_members).filter_by(club_id=club_id).all()
    if members is False:
        session.close()
        raise HTTPException(status_code=409, detail="club has no memberes")

    responce=[]
    for m in members:
        user=session.query(Users).filter_by(id=m.stu_id).first()
        responce.append({
            "member_id":m.id,
            "student_id":m.stu_id,
            "name":user.username,
            "email":user.email,
            "status":m.status,
        })
    session.close()    
    return responce


def create_event(club_id,title,description,venue,event_date,regis_deadline,max_cap,payload):
    session=Session(engine)
    user = session.query(Users).filter_by(email=payload["email"]).first()
    if user is None:
        session.close()
        raise HTTPException(status_code=404,detail="Student Not Found")
    club=session.query(Club).filter_by(id=club_id).first()
    if club is None:
        session.close()
        raise HTTPException(status_code=404,detail="Club Not Found")
    if club.coordinator_id != user.id:
        session.close()
        raise  HTTPException(status_code=403,detail="You are not the club coordinator")

    if regis_deadline > event_date:
        session.close()
        raise  HTTPException(status_code=400,detail="Register deadline cannot be after event date")
    event=Events(
        club_id=club_id,
        title=title,
        description=description,
        venue=venue,
        event_date=event_date,
        regis_deadline=regis_deadline,
        max_cap =max_cap
    )
    session.add(event)
    session.commit()
    session.close()
    return True


def get_events():
    session=Session(engine)
    events=session.query(Events).all()

    resp=[]
    for event in events:
        resp.append({
            "id": event.id,
            "club_id": event.club_id,
            "title": event.title,
            "description": event.description,
            "venue": event.venue,
            "date": event.event_date,
            "regis_deadline": event.regis_deadline,
            "max_cap": event.max_cap
        })

    return resp    
