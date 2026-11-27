from sqlalchemy import create_engine
from sqlalchemy.orm import Session,declarative_base,engine
from fastapi import HTTPException
from datetime import datetime,timedelta,timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel,Field,EmailStr
import os
from AM_functions import Users, Club 


ph=PasswordHasher()

ACCEESS_TOKEN_EXPIRY=120
REFRESH_TOKEN_EXPIRY=7*24*60
ALGORITHM="HS256"
SECRET_KEY=os.getenv("SECRET_KEY")


class CoordinatorRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

def create_token(email, role, token_type):
    time = ACCEESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload = {
        "email": email,
        "token_type": token_type,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time)
    }
    token = jwt.encode(payload=payload,key = SECRET_KEY,algorithm=ALGORITHM)
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


#E1 
def create_coordinator_account(username,password,email):
    session = Session(engine)
    existing_user = session.query(Users).filter_by(email=email).first()
    if existing_user:
        session.close()
        return False
    session.add(Users(username=username, email=email, password=ph.hash(password), role="coordinator"))
    session.commit()
    session.close()
    return True    


#E2
def new_campus_club(name, description, category, coordinator_id):
    session = Session(engine)
    coordinator = session.query(Users).filter_by(id=coordinator_id,role="coordinator").first()
    if not coordinator:
        session.close()
        return False
    new_club = Club(name=name,description=description,category=category,coordinator_id=coordinator_id)
    session.add(new_club)
    session.commit()
    session.close()
    return True

#E3
def available_clubs():
    session = Session(engine)
    clubs  = session.query(Club).all()
    result = []
    for club in clubs:
        result.append({"id": club.id,"name": club.name,"description": club.description,"category": club.category,"coordinator_id": club.coordinator_id})
    session.close()
    return result

#E4
def details_of_club(club_id):
    session = Session(engine)
    club = session.query(Club).filter_by(id=club_id).first()
    if not club:
        session.close()
        return False
    result = {"id": club.id,
              "name": club.name,
              "description": club.description,
              "category": club.category,
              "coordinator_id": club.coordinator_id}
    session.close()
    return result


#E5
def update_club(club_id, email, name, description, category):
    session = Session(engine)
    user = session.query(Users).filter_by(email=email).first()
    if not user or user.role != "coordinator":
        session.close()
        return False
    club = session.query(Club).filter_by(id=club_id).first()
    if not club or club.coordinator_id != user.id:
        session.close()
        return False
    if name is not None:
        club.name = name
    if description is not None:
        club.description = description
    if category is not None:
        club.category = category
    session.commit()
    session.close()
    return True
