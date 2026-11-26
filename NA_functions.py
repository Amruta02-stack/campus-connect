from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date
import jwt
from argon2 import PasswordHasher
from AM_functions import engine, Users, Club, Events, Event_regis, SECRET_KEY, ALGORITHM   

ph=PasswordHasher()

ACCEESS_TOKEN_EXPIRY=120
REFRESH_TOKEN_EXPIRY=7*24*60
SECRET_KEY="SECRET321"
ALGORITHM="HS256"

def registar_user(username,email,password,role):
    email=email.strip().lower()
    role=role.strip().lower()
    if role not in ["admin","student"]:
        raise HTTPException(status_code=422,detail="invalid role type")
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
    reg=Event_regis(event_id=event_id,stu_id=user.id)
    session.add(reg)
    session.commit()
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
    if club.id != event.club_id:
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
    coord=session.query(Users).filter_by(email=email.strip().lower()).first()
    if  coord is None:
        session.close()
        raise HTTPException(status_code=401,detail="User not found")
    event=session.query(Events).filter_by(id=event_id).first()
    if event is None:
        session.close()
        raise HTTPException(status_code=404,detail="Event not found")
    club=session.query(Club).filter_by(id=event.club_id).first()
    if club.id!=event.club_id:
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
    total_attended=0
    for r in regs:
        e=session.query(Events).filter_by(id=r.event_id).first()
        history.append({"event_id":e.id,"title":e.title,"venue":e.venue,"date":e.event_date,"attended":r.attended})
 
        if r.attended:
                total_attended+=1
  
    response={"stu_id":user.id,"total_registered":len(history),
              "total_attended":total_attended,"history":history}
    session.close()
    return response