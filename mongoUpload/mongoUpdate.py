from pymongo.mongo_client import MongoClient
# import schedule
import time
from mongoUpload.mongoConstructorStandings import update_constructor_standings
from mongoUpload.mongoDriverStandings import update_driver_standings
from mongoUpload.mongoEvents import update_results


MONGO_URI = "mongodb+srv://natequan:KlyW0bJBjQfa3Xqb@f1analytics.gspkb73.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "f1Analytics"
CONSTRUCTOR_COLLECTION_NAME = "ConstructorStandings"
DRIVER_COLLECTION_NAME = "DriverStandings"
EVENTS_COLLECTION_NAME = "Events"

# Create a new client and connect to the server
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# imports all the update functions and groups them into one function that updates all the data
def job(): 
    update_constructor_standings(db[CONSTRUCTOR_COLLECTION_NAME])
    update_driver_standings(db[DRIVER_COLLECTION_NAME])
    update_results(db[EVENTS_COLLECTION_NAME])