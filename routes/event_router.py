from fastapi import APIRouter
from models.events import Event
from config.database import db
from schema.event_schema import event_list_serial, event_individual_serial
# from schema.result_schema import race_result_list_serial, race_result_individual_serial, qual_result_individual_serial, qual_result_list_serial
from bson import ObjectId
from datetime import datetime
from typing import Union
import json 

COLLECTION_NAME = "Events"

collection = db[COLLECTION_NAME]

event_router = APIRouter()

# endpoint that gets all events for a given year
@event_router.get("/events/{year}")
def get_events(year: int): 
    # set start and endpoint for all events in a certain year
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    # query events that come between the start and endpoint
    query = collection.find(
        {"EventDate": {"$lte": end_date, "$gte":start_date}}).sort("RoundNumber", 1)
    return event_list_serial(query)

# endpoint that gets an event for a given year and round number
@event_router.get("/event/{year}/{grandPrix}")
def get_event(year: int, grandPrix: str):
    # set start and endpoint for all events in a certain year
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    # query events in between the start and end date with the specified round number
    query = collection.find_one(
        {"EventDate": {"$lte": end_date, "$gte": start_date},  "EventName": grandPrix}
        )
    return event_individual_serial(query)

# endpoint that gets all upcoming events for the current year
@event_router.get("/next")
def get_upcoming_events():
    now = datetime.now()
    # query events that come after "now"
    query = collection.find({"EventDate": {"$gt": now}}).sort({"RoundNumber": 1})
    return event_list_serial(query)

# endpoint that gets the last event
@event_router.get("/last-event")
def get_last_event():
    now = datetime.now()
    # query event where year=current_year and less than "now"
    curr_year = collection.find({"$and": [{"$expr": {"$eq": [{"$year": "$EventDate"}, now.year]}}, {"EventDate": {"$lt": now}}]}).sort({"RoundNumber": 1})
    # checks if there is an event found in the previous query
    count = collection.count_documents({"$and": [{"$expr": {"$eq": [{"$year": "$EventDate"}, now.year]}}, {"EventDate": {"$lt": now}}]})
    
    # if no event is found, then we look at last year's events
    if count == 0: 
        # find last year's events and sort in opposite order
        last_year = collection.find({"$expr": {"$eq": [{"$year": "$EventDate"}, now.year - 1]}}).sort({"RoundNumber": -1})
        # last event must be the first record in the sorted query
        last_event = last_year[0]
        return event_individual_serial(last_event)
    else:
        return event_individual_serial(curr_year)

