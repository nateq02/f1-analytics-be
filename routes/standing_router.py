from fastapi import APIRouter
from models.standings import (DriverStandingObj, ConstructorStandingObj)
from config.database import db
from schema.standing_schema import (driver_standing_event_list_serial, constructor_standing_event_list_serial)
from bson import ObjectId
from datetime import datetime
from typing import Union


DRIVER_STANDING_COLLECTION_NAME = "DriverStandings"
CONSTRUCTOR_STANDING_COLLECTION_NAME = "ConstructorStandings"

driverStandingCollection = db[DRIVER_STANDING_COLLECTION_NAME]
constructorStandingCollection = db[CONSTRUCTOR_STANDING_COLLECTION_NAME]

standing_router = APIRouter()

@standing_router.get("/driver-standings/{year}")
def get_driver_standings(year: Union[int, str]):
    if year != "current":
        driver_standings = driverStandingCollection.find({"year": year}).sort({"position": 1})
    else:
        max_year_doc =  driverStandingCollection.aggregate([
            {
                "$group": {
                    "_id": None,
                    "max_year": {"$max": "$year"}
                }
            }
        ])
        for document in max_year_doc: 
            max_year = document.get("max_year", 0)
        
        driver_standings = driverStandingCollection.find({"year": max_year}).sort({"position": 1})
    
    return driver_standing_event_list_serial(driver_standings)

@standing_router.get("/constructor-standings/{year}")
def get_constructor_standings(year: Union[int, str]):
    if year != "current":
        constructor_standings = constructorStandingCollection.find({"year": year}).sort({"position": 1})
    else: 
        max_year_doc = constructorStandingCollection.aggregate([
            {
                "$group": {
                    "_id": None,
                    "max_year": {"$max": "$year"}
                }
            }
        ])
        for document in max_year_doc:
            max_year = document.get("max_year", 0)
        
        constructor_standings = constructorStandingCollection.find({"year": max_year}).sort({"position": 1})
    
    return constructor_standing_event_list_serial(constructor_standings)
