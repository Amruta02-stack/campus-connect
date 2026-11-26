from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
import NA_functions as function
app = FastAPI(title="Campus Connect")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserIn(BaseModel):
    username: str = Field(min_length=1)
    role :str 
    email: EmailStr
    password: str = Field(min_length=8)

class Attend(BaseModel):
    stu_id: int
    attended: bool = True


# A1  Register a new account
@app.post("/auth/register")
def register(u: UserIn):
    user = function.registar_user(u.username, u.email, u.password,u.role)
    if user is None:
        raise HTTPException(status_code=409, detail="Email already registered")
    return {"message": "User registered successfully", "user": user}


# E11  Register for an event ->stu
@app.post("/events/{event_id}/register")
def register_event(event_id: int, token=Header(None)):
    payload = function.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    if payload["role"] != "student":
        raise HTTPException(status_code=403, detail="Not allowed for your role")
    return function.register_for_event(email=payload["email"], event_id=event_id)


# E12 Cancel event registration ->stu
@app.delete("/events/{event_id}/register")
def cancel_event(event_id: int, token=Header(None)):
    payload = function.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    if payload["role"] != "student":
        raise HTTPException(status_code=403, detail="Not allowed for your role")
    return function.cancel_registration(email=payload["email"], event_id=event_id)


# E13 Mark event attendance ->club coord
@app.patch("/events/{event_id}/attendance")
def attendance(event_id: int, body: Attend, token=Header(None)):
    event_attend = function.verify_token(token=token, token_type="access")
    if not event_attend:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    if event_attend["role"] != "coordinator":
        raise HTTPException(status_code=403, detail="Not allowed for your role")
    return function.mark_attendance(email=event_attend["email"], event_id=event_id, stu_id=body.stu_id, attended=body.attended)

# E14  Get registered participants for an event -> club coord
@app.get("/events/{event_id}/participants")
def participants(event_id: int, token=Header(None)):
    payload = function.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    if payload["role"] != "coordinator":
        raise HTTPException(status_code=403, detail="Not allowed for your role")
    return function.get_event_participants(email=payload["email"], event_id=event_id)


# E15   Get a student's event participation history ->stu
@app.get("/students/participation")
def participation(token=Header(None)):
    history = function.verify_token(token=token, token_type="access")
    if not history:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    if history["role"] != "student":
        raise HTTPException(status_code=403, detail="Not allowed for your role")
    return function.get_participation_history(email=history["email"])


# @app.post("/auth/login")
# def login(l:function.LoginIn):
#     token=function.verify_login(email=l.email,password=l.password)
#     if not token:
#         raise HTTPException(status_code=401,detail="Access denied")
#     return token

# # A3
# @app.post("/auth/refresh")
# def refresh(refresh_token: str = Header(None)):
#     payload = function.verify_token(token=refresh_token,token_type="refresh")
#     if not payload:
#         raise HTTPException(status_code=401,detail="Invalid or expired refresh token")
#     access_token = function.create_token(username=payload["username"],user_type=payload["user_type"],token_type="access")
#     return {"access_token": access_token}

# #E1
# @app.post("/coordinators")
# def create_coordinator(user: function.CoordinatorRequest, token=Header(None)):
#     payload = function.verify_token(token, "access")
#     if not payload or payload["user_type"] != "admin":
#         raise HTTPException(status_code=403, detail="Access denied")
#     result = function.create_coordinator_account(username=user.username,email=user.email,password=user.password)
#     if not result:
#         raise HTTPException(status_code=409, detail="Username already exists")
#     return {"message": "Coordinator created successfully"}

# #E2
# @app.post("/clubs")  
# def new_campus_clubs(club: function.ClubIn ,token=Header(None)):
#     payload = function.verify_token(token, "access")
#     if not payload or payload["user_type"] != "admin":
#         raise HTTPException(status_code=403, detail="Access denied")
#     result = function.new_campus_club(name=club.name,description=club.description,category=club.category,coordinator_id=club.coordinator_id)
#     if not result:
#         raise HTTPException(status_code=404,detail="Coordinator not found")
#     return {"message": "Campus club created successfully"}

# #E3
# @app.get("/clubs")
# def available_clubs():
#     return function.available_clubs()


# #E4
# @app.get("/clubs/{club_id}")
# def details_of_club(club_id:int):
#     result = function.details_of_club(club_id)
#     if not result:
#         raise HTTPException(status_code=404,detail="Club not found")
#     return result


# # E5
# @app.patch("/clubs/{club_id}")
# def update_club_info(club_id: int, club: function.ClubUpdate, token=Header(None)):
#     payload = function.verify_token(token, "access")
#     if not payload:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     if payload["user_type"] != "coordinator":
#         raise HTTPException(status_code=403, detail="Coordinator access required")
#     result = function.update_club(club_id=club_id,username=payload["username"],name=club.name,description=club.description,category=club.category)
#     if not result:
#         raise HTTPException(status_code=403, detail="You cannot update this club")
#     return {"message": "Club updated successfully"}