from fastapi import APIRouter
from models.standings import (DriverStandingObj, ConstructorStandingObj)
from config.database import db
from schema.standing_schema import (driver_standing_event_list_serial, constructor_standing_event_list_serial)
from bson import ObjectId
from datetime import datetime

DRIVER_STANDING_COLLECTION_NAME = "DriverStandings"
CONSTRUCTOR_STANDING_COLLECTION_NAME = "ConstructorStandings"

driverStandingCollection = db[DRIVER_STANDING_COLLECTION_NAME]
constructorStandingCollection = db[CONSTRUCTOR_STANDING_COLLECTION_NAME]

standing_router = APIRouter()

@standing_router.get("/driver-standings/{year}")
def get_driver_standings(year: int):
    driver_standings = driverStandingCollection.find({"year": year}).sort({"position": 1})
    return driver_standing_event_list_serial(driver_standings)

@standing_router.get("/constructor-standings/{year}")
def get_constructor_standings(year: int):
    constructor_standings = constructorStandingCollection.find({"year": year}).sort({"position": 1})
    return constructor_standing_event_list_serial(constructor_standings)

