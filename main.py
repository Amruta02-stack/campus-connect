from fastapi import FastAPI,HTTPException,Header,Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import Optional
import NA_functions as n
import AM_functions as a
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def authorize(token,roles):
    registar=n.verify_token(token=token,token_type="access")
    if not registar:
        raise HTTPException(status_code=401,detail="Invalid or Expired access token")
    if registar["role"] not in roles:
        raise HTTPException(status_code=403,detail="Not allowed for your role")
    return registar

@app.post("/auth/register")
def registar(u: a.UserIn):
    user = n.registar_user(u.username, u.email, u.password)
    if user is None:
        raise HTTPException(status_code=409, detail="Email already registered")
    return {"message": "User registered successfully", "user": user}
