from fastapi import APIRouter
from models.events import Event
from config.database import db
from schema.schemas import list_serial
from bson import ObjectId

COLLECTION_NAME = "F1Events"

collection = db[COLLECTION_NAME]

event_router = APIRouter()

# GET test - gets all events in the database
@event_router.get("/test")
def get_events2():
    events = list_serial(collection.find())
    return events

# endpoint that gets all events for a given year
@event_router.get("/events/{year}")
def get_events(year: int): 
    query = collection.find({"$expr": {"$eq": [{"$year": "$EventDate"}, year]}})
    return list_serial(query)