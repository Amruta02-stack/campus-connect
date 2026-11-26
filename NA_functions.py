from sqlalchemy import create_engine,Integer,String,Date,Column,ForeignKey,Boolean
from sqlalchemy.orm import Session,declarative_base
from fastapi import FastAPI,HTTPException
from datetime import date,datetime,timedelta,timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel,Field,EmailStr
from typing import Optional   

# import SU_functions as s

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

class CoordinatorRequest(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=8)    

Base.metadata.create_all(engine)



# def verify_token(token, token_type):
#     if not token:
#         return False
#     try:
#         payload = jwt.decode(jwt=token,key=SECRET_KEY,algorithms=[ALGORITHM])
#     except jwt.InvalidTokenError:
#         return False
#     if payload.get("token_type") == token_type:
#         return payload
#     return False

# def create_admin():
#     session = Session(engine)
#     existing_admin = session.query(Users).filter_by( email="admin@gmail.com").first()
#     if not existing_admin:
#         admin = Users(username="admin",email="admin@gmail.com",password=ph.hash("admin12345"),role="admin")
#         session.add(admin)
#         session.commit()
#     session.close()

# #E1 
# def create_coordinator_account(username,password,email):
#     session = Session(engine)
#     existing_user = session.query(Users).filter_by(username=username).first()
#     if existing_user:
#         session.close()
#         return False
#     session.add(Users(username=username, email=email, password=ph.hash(password), role="coordinator"))
#     session.commit()
#     session.close()
#     return True

# #E2
# def new_campus_club(name, description, category, coordinator_id):
#     session = Session(engine)
#     coordinator = session.query(Users).filter_by(id=coordinator_id,role="coordinator").first()
#     if not coordinator:
#         session.close()
#         return False
#     new_club = Club(name=name,description=description,category=category,coordinator_id=coordinator_id)
#     session.add(new_club)
#     session.commit()
#     session.close()
#     return True


# #E3
# def available_clubs():
#     session = Session(engine)
#     clubs  = session.query(Club).all()
#     result = []
#     for club in clubs:
#         result.append({"id": club.id,"name": club.name,"description": club.description,"category": club.category,"coordinator_id": club.coordinator_id})
#     session.close()
#     return result


# #E4
# def details_of_club(club_id):
#     session = Session(engine)
#     club = session.query(Club).filter_by(id=club_id).first()
#     if not club:
#         session.close()
#         return False
#     result = {"id": club.id,
#               "name": club.name,
#               "description": club.description,
#               "category": club.category,
#               "coordinator_id": club.coordinator_id}
#     session.close()
#     return result

# #E5
# def update_club(club_id, username, name, description, category):
#     session = Session(engine)
#     user = session.query(Users).filter_by(username=username).first()
#     if not user or user.role != "coordinator":
#         session.close()
#         return False
#     club = session.query(Club).filter_by(id=club_id).first()
#     if not club or club.coordinator_id != user.id:
#         session.close()
#         return False
#     if name is not None:
#         club.name = name
#     if description is not None:
#         club.description = description
#     if category is not None:
#         club.category = category
#     session.commit()
#     session.close()
#     return True

def registar_user(username,email,password,role):
    email=email.strip().lower()
    session=Session(engine)
    if session.query(Users).filter_by(email=email).first():
        session.close()
        return None
    user=Users(username=username,email=email,password=ph.hash(password),role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    response={"id":user.id,"username":user.username,"email":user.email,"role":user.role}
    session.close()
    return response

def register_for_event(email,event_id):
    session=Session(engine)
    user=session.query(Users).filter_by(email=email.strip().lower()).first()
    if user is None:
        session.close()
        raise HTTPException(status_code=401,detail="User not found")
    event=session.query(Events).filter_by(id=event_id).first()
    if event is None:
        session.close()
        raise HTTPException(status_code=404,detail="Event not found")
    if date.today()>event.regis_deadline:
        session.close()
        raise HTTPException(status_code=400,detail="Registration deadline has passed")
    # existing=session.query(Event_regis).filter_by(event_id=event_id,stu_id=user.id).first()
    # if existing and existing.status=="registered":
    #     session.close()
    #     raise HTTPException(status_code=409,detail="Already registered for this event")
    # taken=len(session.query(Event_regis).filter_by(event_id=event_id,status="registered").all())
    # if taken>=event.max_cap:
    #     session.close()
    #     raise HTTPException(status_code=409,detail="Event is full")
    # if existing:
    #     existing.status="registered"
    #     existing.attended=False
    #     reg=existing
    
    reg=Event_regis(event_id=event_id,stu_id=user.id)
    session.add(reg)
    session.commit()
    # session.refresh(reg)
    response={"registration_id":reg.id,"event_id":reg.event_id,"status":reg.status,"attended":reg.attended}
    session.close()
    return response

#E12
def cancel_registration(email,event_id):
    session=Session(engine)
    user=session.query(Users).filter_by(email=email.strip().lower()).first()
    if user is None:
        session.close()
        raise HTTPException(status_code=401,detail="User not found")
    event_reg=session.query(Event_regis).filter_by(event_id=event_id,stu_id=user.id,status="registered").first()
    if event_reg is None:
        session.close()
        raise HTTPException(status_code=404,detail="No active registration found")
    if event_reg.attended:
        session.close()
        raise HTTPException(status_code=400,detail="Cannot cancel after attendance is marked")
    event_reg.status="cancelled"
    session.commit()
    session.close()
    return {"event_id":event_id,"status":"cancelled"}

#E13
def mark_attendance(email,event_id,stu_id,attended):
    session=Session(engine)
    create_coordinator=session.query(Users).filter_by(email=email.strip().lower()).first()
    if create_coordinator is None:
        session.close()
        raise HTTPException(status_code=401,detail="User not found")
    event=session.query(Events).filter_by(id=event_id).first()
    if event is None:
        session.close()
        raise HTTPException(status_code=404,detail="Event not found")
    club=session.query(Club).filter_by(id=event.club_id).first()
    if club.create_coordinator_id!=create_coordinator.id:
        session.close()
        raise HTTPException(status_code=403,detail="This event does not belong to your club")
    event_reg=session.query(Event_regis).filter_by(event_id=event_id,stu_id=stu_id,status="registered").first()
    if event_reg is None:
        session.close()
        raise HTTPException(status_code=404,detail="Student is not registered for this event")
    event_reg.attended=attended
    session.commit()
    response={"event_id":event_id,"stu_id":stu_id,"attended":event_reg.attended}
    session.close()
    return response

#E14
def get_event_participants(email,event_id):
    session=Session(engine)
    create_coordinator=session.query(Users).filter_by(email=email.strip().lower()).first()
    if create_coordinator is None:
        session.close()
        raise HTTPException(status_code=401,detail="User not found")
    event=session.query(Events).filter_by(id=event_id).first()
    if event is None:
        session.close()
        raise HTTPException(status_code=404,detail="Event not found")
    club=session.query(Club).filter_by(id=event.club_id).first()
    if club.create_coordinator_id!=create_coordinator.id:
        session.close()
        raise HTTPException(status_code=403,detail="This event does not belong to your club")
    event_regs=session.query(Event_regis).filter_by(event_id=event_id,status="registered").all()
    participants=[]
    for r in event_regs:
        student=session.query(Users).filter_by(id=r.stu_id).first()
        participants.append({"stu_id":student.id,"username":student.username,"email":student.email,"attended":r.attended})
    response={"event_id":event.id,"title":event.title,"max_cap":event.max_cap,
              "registered_count":len(participants),"participants":participants}
    session.close()
    return response

#E15
def get_participation_history(email):
    session=Session(engine)
    user=session.query(Users).filter_by(email=email.strip().lower()).first()
    if user is None:
        session.close()
        raise HTTPException(status_code=401,detail="User not found")
    regs=session.query(Event_regis).filter_by(stu_id=user.id,status="registered").all()
    history=[]
    for r in regs:
        e=session.query(Events).filter_by(id=r.event_id).first()
        history.append({"event_id":e.id,"title":e.title,"venue":e.venue,"date":e.date,"attended":r.attended})
    history.sort(key=lambda h:h["date"],reverse=True)
    response={"stu_id":user.id,"total_registered":len(history),
              "total_attended":len([h for h in history if h["attended"]]),"history":history}
    session.close()
    return response