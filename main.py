from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # used to give permission to front-end
import fastf1 as f1
from fastf1.ergast import Ergast
import pandas as pd
import json
import datetime

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
    f1.Cache.enable_cache('/Users/natequan/Desktop/Fall2023/OPIM4996/f1-analytics/f1-analytics-be/cache')
    
    # calls get_driver_standings from Ergast
        # need to call .content[0] to retreive the content
            # data is stored in an array of multiple data frames hence the [0]
    standings = ergast.get_driver_standings(season='current').content[0]

    # convert the standings df to json
        # orient parameter is used to store each record in its own dictionary
    return standings.to_json(orient = 'records')

@app.get("/constructor-standings")
def get_constructor_standings():
    # enables cache, maybe move outside of the function
    f1.Cache.enable_cache('/Users/natequan/Desktop/Fall2023/OPIM4996/f1-analytics/f1-analytics-be/cache')
    
    # calls get_constructor_standings from Ergast
        # need to call .content[0] to retreive the content
            # data is stored in an array of multiple data frames hence the [0]
    standings = ergast.get_constructor_standings(season='current').content[0]

    # convert the standings df to json
        # orient parameter is used to store each record in its own dictionary
    return standings.to_json(orient = 'records')

@app.get("/next")
def get_next_session():
    # enables cache
    f1.Cache.enable_cache('/Users/natequan/Desktop/Fall2023/OPIM4996/f1-analytics/f1-analytics-be/cache')
    
    # gets the upcoming events, returned as an events type object
    upcoming = f1.get_events_remaining()

    # converts the events object into a dictionary of records
        # upcoming_list is a list of dictionaries, each dictionary is a record
    upcoming_list = upcoming.to_dict(orient = 'records')

    # Timestamps are not able to be converted to JSON, so need to remove them by converting to string
    for event in upcoming_list:
        for key, value in event.items():
            if isinstance(value, datetime.datetime):
                value = str(value)
                event[key] = value

    # converts the list of dictionaries into a JSON 
    upcoming_json = json.dumps(upcoming_list)
    
    return upcoming_json

# function to get round number of a past event
def get_past_event():
    f1.Cache.enable_cache('/Users/natequan/Library/Caches/fastf1')
    schedule = ergast.get_race_schedule(season="current")
    last_round = None

    now = datetime.datetime.now()

    for index, event in schedule.iterrows():
        if event['raceDate'] < now:
            last_round = event['round']
        else:
            return int(last_round)

# gets results of the last race
@app.get('/last-race-results')
def get_past_results():
    f1.Cache.enable_cache('/Users/natequan/Library/Caches/fastf1')
    last_round = get_past_event()
    
    results = ergast.get_race_results(season="current", round=last_round)
    results_content = results.content[0]
    json_results = results_content.to_json(orient='records')

    return json_results
