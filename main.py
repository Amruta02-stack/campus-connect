from fastapi import FastAPI, HTTPException,Header,Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
import SU_functions as s

app = FastAPI()

# A3 - Generate a new access token

@app.post("/refresh")
def refresh_token(refresh_token=Header(None)):
    payload = s.verify_token(token=refresh_token,token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or token expired")
    access_token = s.create_token(email=payload["email"],token_type="access")
    return {"access_token": access_token}

