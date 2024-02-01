from fastapi import APIRouter
from models.events import Event
from config.database import db
from schema.event_schema import event_list_serial
from bson import ObjectId
from datetime import datetime

COLLECTION_NAME = "Schedule"

collection = db[COLLECTION_NAME]

event_router = APIRouter()

# GET test - gets all events in the database
@event_router.get("/test")
def get_events2():
    events = event_list_serial(collection.find())
    return events

# endpoint that gets all events for a given year
@event_router.get("/events/{year}")
def get_events(year: int): 
    query = collection.find({"$expr": {"$eq": [{"$year": "$EventDate"}, year]}})
    return event_list_serial(query)

# endpoint that gets all upcoming events for the current year
@event_router.get("/next")
def get_upcoming_events():
    now = datetime.now()
    query = collection.find({"EventDate": {"$gt": now}}).sort({"RoundNumber": 1})
    return event_list_serial(query)
