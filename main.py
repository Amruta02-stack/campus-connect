from fastapi import FastAPI,HTTPException,Header,Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import Optional
import AM_functions as a

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
def login(l:a.loginIn):
    token=a.verify_login(username=l.username,password=l.password)
    if not token:
        raise HTTPException(status_code=401,detail="Access denied")
    return token

