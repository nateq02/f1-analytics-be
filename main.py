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
)

client = MongoClient("mongodb+srv://natequan:KlyW0bJBjQfa3Xqb@f1analytics.gspkb73.mongodb.net/?retryWrites=true&w=majority")
db = client["f1Analytics"]
event_coll = db["F1Events"]
event_docs = event_coll.find()

@app.get("/")
def home():
    return "Home Page for a Formula 1 Analytics Web App"

# @app.get("/driver-standings")
# def get_driver_standings():
#     # enables cache, maybe move outside of the function
#     f1.Cache.enable_cache('/Users/natequan/Desktop/School/Thesis/f1-analytics/f1-analytics-be/cache')
    
#     # calls get_driver_standings from Ergast
#         # need to call .content[0] to retreive the content
#             # data is stored in an array of multiple data frames hence the [0]
#     # standings = ergast.get_driver_standings(season='current').content[0]
#     standings = ergast.get_driver_standings(season='current').content[0]

#     # convert the standings df to json
#         # orient parameter is used to store each record in its own dictionary
#     return standings.to_json(orient = 'records')

# @app.get("/constructor-standings")
# def get_constructor_standings():
#     # enables cache, maybe move outside of the function
#     f1.Cache.enable_cache('/Users/natequan/Desktop/School/Thesis/f1-analytics/f1-analytics-be/cache')
    
#     # calls get_constructor_standings from Ergast
#         # need to call .content[0] to retreive the content
#             # data is stored in an array of multiple data frames hence the [0]
#     standings = ergast.get_constructor_standings(season='current').content[0]

#     # convert the standings df to json
#         # orient parameter is used to store each record in its own dictionary
#     return standings.to_json(orient = 'records')

# @app.get("/next")
# def get_next_session():
#     # enables cache
#     f1.Cache.enable_cache('/Users/natequan/Desktop/School/Thesis/f1-analytics/f1-analytics-be/cache')
    
#     # gets the upcoming events, returned as an events type object
#     upcoming = f1.get_events_remaining()

#     # converts the events object into a dictionary of records
#         # upcoming_list is a list of dictionaries, each dictionary is a record
#     upcoming_list = upcoming.to_dict(orient = 'records')

#     # Timestamps are not able to be converted to JSON, so need to remove them by converting to string
#     for event in upcoming_list:
#         for key, value in event.items():
#             if isinstance(value, datetime.datetime):
#                 value = str(value)
#                 event[key] = value

#     # converts the list of dictionaries into a JSON 
#     upcoming_json = json.dumps(upcoming_list)
    
#     return upcoming_json

# function to get round number of a past event
def get_past_event():
    f1.Cache.enable_cache('/Users/natequan/Desktop/School/Thesis/f1-analytics/f1-analytics-be/cache')
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
    f1.Cache.enable_cache('/Users/natequan/Desktop/School/Thesis/f1-analytics/f1-analytics-be/cache')
    last_round = get_past_event()

    results = ergast.get_race_results(season="current", round=last_round)
    results_content = results.content[0]
    json_results = results_content.to_json(orient='records')

    return json_results

# need to create an endpoint that contains all circuit data
# need to get all distinct track's data somehow
# for now, we will just use the next event
@app.get('/circuit-info')
def get_next_circuit():
    f1.Cache.enable_cache('/Users/natequan/Desktop/School/Thesis/f1-analytics/f1-analytics-be/cache')
    session = f1.get_session(2023, 'Silverstone', 'Q')
    session.load()
    circuit_info = session.get_circuit_info()

    corners = circuit_info.corners.to_json(orient='records')
    # rotation = circuit_info.rotation.to_json(orient='records')

    # return circuit_info.rotation
    return json.dumps({'corners': corners, 'rotation': circuit_info.rotation})

@app.get('/fastest-lap-info')
def get_fastest_lap():
    f1.Cache.enable_cache('/Users/natequan/Desktop/School/Thesis/f1-analytics/f1-analytics-be/cache')
    session = f1.get_session(2023, 'Silverstone', 'Q')
    session.load()

    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()

    return pos.to_json(orient='records')

@app.get('/results/{year}/{circuit}/{session}')
def get_results(year: int, circuit: Union[int,str], session: str):
    f1.Cache.enable_cache('/Users/natequan/Desktop/School/Thesis/f1-analytics/f1-analytics-be/cache')
    weekend = f1.get_session(year, circuit, session)
    weekend.load()
    
    results = weekend.results

    return results.to_json(orient='records')

@app.get('/event/{year}/{circuit}/{session}')
def get_info(year: int, circuit: Union[int,str], session: str):
    f1.Cache.enable_cache('/Users/natequan/Desktop/School/Thesis/f1-analytics/f1-analytics-be/cache')
    weekend = f1.get_session(year, circuit, session)
    weekend.load()
    
    event = weekend.event

    return event.to_json() 

# @app.get('/last-event')
# def get_last_event():
# @app.get('/schedule/{year}')
# def get_schedule(year:int):
#     f1.Cache.enable_cache('/Users/natequan/Desktop/School/Thesis/f1-analytics/f1-analytics-be/cache')
#     schedule = f1.get_event_schedule(year)

#     return schedule.to_json(orient='records')

# @app.get('/test')
# def get_event():
#     most_recent = event_coll.find_one()
#     return most_recent
app.include_router(event_router)
app.include_router(standing_router)