from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # used to give permission to front-end
import fastf1 as Fastf1
from fastf1.ergast import Ergast
import pandas as pd

app = FastAPI()

ergast = Ergast()

# Gives permission to all requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get("/")
def home():
    return "Home Page for a Formula 1 Analytics Web App"

@app.get("/driver-standings")
def get_driver_standings():
    # enables cache, maybe move outside of the function
    Fastf1.Cache.enable_cache('/Users/natequan/Desktop/Fall2023/OPIM4996/f1-analytics/f1-analytics-be/cache')
    
    # calls get_driver_standings from Ergast
        # need to call .content[0] to retreive the content
            # data is stored in an array of multiple data frames hence the [0]
    standings = ergast.get_driver_standings(season='current').content[0]

    # convert the standings df to json
        # orient parameter is used to store each record in its own dictionary
        #    with each field:value pair
    return standings.to_json(orient = 'table')

@app.get("/next")
def get_next_session():
    Fastf1.Cache.enable_cache('/Users/natequan/Desktop/Fall2023/OPIM4996/f1-analytics/f1-analytics-be/cache')
    upcoming = Fastf1.get_events_remaining()
    next_event = upcoming.iloc[0]
    next_dict = next_event.to_dict()
    return next_dict