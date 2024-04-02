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

# end point to get the driver standings for a particular year
@standing_router.get("/driver-standings/{year}")
def get_driver_standings(year: Union[int, str]):
    # if year is not "current" in the url, then get the year's results in the url
    if year != "current":
        driver_standings = driverStandingCollection.find({"year": int(year)}).sort({"position": 1})
    
    # if the year in the url is "current", get the current year's results
    else:
        # query to get the max year in the driver standing collection -> the max year is the current year
        max_year_doc =  driverStandingCollection.aggregate([
            {
                "$group": {
                    "_id": None,
                    "max_year": {"$max": "$year"}
                }
            }
        ])
        # get the year as an integer, rather than cursor
        for document in max_year_doc: 
            max_year = document.get("max_year", 0)
        
        # find records where the year is the max year (current year) and sort by position
        driver_standings = driverStandingCollection.find({"year": max_year}).sort({"position": 1})
    
    return driver_standing_event_list_serial(driver_standings)

# end point to get the constructor standings for a particular year
@standing_router.get("/constructor-standings/{year}")
def get_constructor_standings(year: Union[int, str]):
    # if year is not "current" in the url, then get the year's results in the url
    if year != "current":
        constructor_standings = constructorStandingCollection.find({"year": int(year)}).sort({"position": 1})
    
    # if the year is "current" in the url, get the current year's results
    else: 
        # finds the max year in the collection, which is the current year
        max_year_doc = constructorStandingCollection.aggregate([
            {
                "$group": {
                    "_id": None,
                    "max_year": {"$max": "$year"}
                }
            }
        ])

        # gets the current year as an int and not a cursor
        for document in max_year_doc:
            max_year = document.get("max_year", 0)
        
        # queries the results with the current year and orders by the position
        constructor_standings = constructorStandingCollection.find({"year": max_year}).sort({"position": 1})
    
    return constructor_standing_event_list_serial(constructor_standings)
