from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # used to give permission to front-end
import fastf1 as f1
from fastf1.ergast import Ergast
from pymongo import MongoClient
import pandas as pd
import json
import datetime
from typing import Union
from routes.event_router import event_router
from routes.standing_router import standing_router

# python3 -m uvicorn main:app --reload
# using virtual environment: source venv/bin/activate

app = FastAPI()
ergast = Ergast()

# Gives permission to all requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb+srv://natequan:KlyW0bJBjQfa3Xqb@f1analytics.gspkb73.mongodb.net/?retryWrites=true&w=majority")
db = client["f1Analytics"]
event_coll = db["F1Events"]
event_docs = event_coll.find()

@app.get("/")
def home():
    return "Home Page for a Formula 1 Analytics Web App"


app.include_router(event_router)
app.include_router(standing_router)