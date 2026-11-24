from fastapi import FastAPI, HTTPException, Header , Body
from fastapi.middleware.cors import CORSMiddleware
import function
app = FastAPI(title="Campus Connect API", description="Clubs and events management platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALL = ["admin", "coordinator", "student"]

def authorize(token, roles):
    campus = function.verify_token(token=token, token_type="access")
    if not campus:
        raise HTTPException(status_code=401, detail="Invalid or Expired access token")
    if campus["role"] not in roles:
        raise HTTPException(status_code=403, detail="Not allowed for your role")
    return campus
