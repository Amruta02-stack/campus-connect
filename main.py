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

