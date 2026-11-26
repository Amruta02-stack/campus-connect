from fastapi import FastAPI,HTTPException,Header,Body
from fastapi.middleware.cors import CORSMiddleware

import SU_functions as s
import AM_functions as a
import NA_functions as n

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



# A3
@app.post("/auth/refresh")
def refresh(refresh_token: str = Header(None)):
    payload = s.verify_token(token=refresh_token,token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or expired refresh token")
    access_token = s.create_token(username=payload["username"],user_type=payload["user_type"],token_type="access")
    return {"access_token": access_token}

#E1
@app.post("/coordinators")
def create_coordinator(user: s.CoordinatorRequest, token=Header(None)):
    payload = s.verify_token(token, "access")
    if not payload or payload["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    result = s.create_coordinator_account(username=user.username,email=user.email,password=user.password)
    if not result:
        raise HTTPException(status_code=409, detail="Username already exists")
    return {"message": "Coordinator created successfully"}


#E2
@app.post("/clubs")  
def new_campus_clubs(club: a.ClubIn ,token=Header(None)):
    payload = s.verify_token(token, "access")
    if not payload or payload["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    result = s.new_campus_club(name=club.name,description=club.description,category=club.category,coordinator_id=club.coordinator_id)
    if not result:
        raise HTTPException(status_code=404,detail="Coordinator not found")
    return {"message": "Campus club created successfully"}


#E3
@app.get("/clubs")
def available_clubs():
    return s.available_clubs()