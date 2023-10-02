from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # used to give permission to front-end
import fastf1
import pandas as pd

app = FastAPI()

# Gives permission to all requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get("/")
def home():
    return "Home Page for a Formula 1 Analytics Web App"



@app.get("/next")
async def get_next_session():
    fastf1.Cache.enable_cache('/Users/natequan/Desktop/Fall2023/OPIM4996/f1-analytics/f1-analytics-be/cache')
    upcoming = fastf1.get_events_remaining()
    next_event = upcoming.iloc[0]
    next_dict = next_event.to_dict()
    return next_dict