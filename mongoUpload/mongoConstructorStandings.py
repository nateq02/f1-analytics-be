from pymongo.mongo_client import MongoClient
import fastf1 as f1
from fastf1.ergast import Ergast
from datetime import datetime
import pandas as pd

# for running in shell
# mongosh "mongodb+srv://f1analytics.gspkb73.mongodb.net/" --apiVersion 1 --username natequan

MONGO_URI = "mongodb+srv://natequan:KlyW0bJBjQfa3Xqb@f1analytics.gspkb73.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "f1Analytics"
COLLECTION_NAME = "ConstructorStandings"

# Create a new client and connect to the server
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Testing connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# connects to Ergast API to get constructor standings data
ergast = Ergast()

# function to load a year's constructor standings
def load_constructor_standings(year):
    # get the constructor standings data
    standings = ergast.get_constructor_standings(season = year).content[0]
    # since there's no year field, include that
    standings["year"] = year
    # insert the data into the database
    collection.insert_many(standings.to_dict(orient="records"))

# function to delete the current schedule data in mongo
def delete_constructor_standings():
    collection.delete_many({})

def update_constructor_standings():
    # gets the current standings
    current_standings = ergast.get_constructor_standings(season = "current").content[0]
    # gets the current year
    current_year = datetime.now().year

    # query the max year in the database
        # groups all the records into one group and takes the max year
    result = collection.aggregate([
        {
            "$group": {
                "_id": None,
                "max_year": {"$max": {"$year": "$EventDate"}}
            }
        }
    ])
    # gets the max_year
    for document in result:
        max_year = document.get("max_year", 0)
    
    # get the max points from the most recent season for comparison
    latest_max_points = collection.find({ "year": max_year, "position": 1}, {"points": 1, "_id": 0})

    # gets the current_standings max points
    curr_max_points = current_standings.iloc[0]["points"]

    # if the two max_points values aren't equal:
        # 1 - Current year standings need to be updated
        # 2 - It's changing from last year to the current year
    if latest_max_points != curr_max_points: 
        # Case 1: deletes all of this years values and updates them
        if (current_year == max_year):
            collection.delete_many( { "year": max_year} )
            collection.insert_many(current_standings)
        # Case 2: keeps all of the max year's values, adds the current year standings
        else: 
            current_standings["year"] = current_year - 1
            collection.insert_many(current_standings.to_dict(orient="records"))

delete_constructor_standings()

for year in range(2010, 2023):
    load_constructor_standings(year)

update_constructor_standings()

client.close()