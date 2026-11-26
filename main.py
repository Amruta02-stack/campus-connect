from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import FunctionFilter
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
