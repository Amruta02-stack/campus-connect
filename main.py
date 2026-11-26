from fastapi import FastAPI,HTTPException,Header,Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import Optional
import AM_functions as a
import SU_functions as s

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
def login(l:a.LoginIn):
    token=a.verify_login(email=l.email,password=l.password)
    if not token:
        raise HTTPException(status_code=401,detail="Access denied")
    return token

@app.post("/clubs/{club_id}")
def register_package(club_id: int,token=Header(None)):
    payload = s.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")
    if payload["role"] != "student":
        raise HTTPException(status_code=403,detail="Access denied")
    if a.apply_club(club_id,payload):
        return {"message": "Applied to clud successful"}

@app.patch("/clubs/{club_id}/members/{member_id}")
def decide_membership(club_id: int,member_id: int,status: str ,token=Header(None)):
    payload = s.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")
    if payload["role"] != "club_coordinator":
        raise HTTPException(status_code=403,detail="Access denied")
    if a.decide_membership(status,payload,member_id,club_id):
        return {"message": f"Updated the membership status as {status}"}


@app.get("/clubs/{club_id}")
def get_club_members(club_id: int,token=Header(None)):
    payload = s.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")
    if payload["role"] != "club_coordinator":
        raise HTTPException(status_code=403,detail="Access denied")
    return a.get_club_members(club_id=club_id,payload=payload)

@app.post("/events")
def create_event(club_id:int,e:a.EventIn,token=Header(None)):
    payload = s.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")
    if payload["role"] != "club_coordinator":
        raise HTTPException(status_code=403,detail="Access denied")
    if a.create_event(club_id,e.title,e.description,e.venue,e.event_date,e.regis_deadline,e.max_cap,payload=payload):
        return {"message:": "Event registered successful"}
    
@app.get("/events")
def all_events():
    return a.get_events()
    