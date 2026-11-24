from fastapi import FastAPI, HTTPException,Header,Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
import SU_functions as s

app = FastAPI()

# A3 - Generate a new access token



