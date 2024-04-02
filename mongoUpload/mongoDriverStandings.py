from pymongo.mongo_client import MongoClient
import fastf1 as f1
from fastf1.ergast import Ergast
from datetime import datetime
import pandas as pd

# for running in shell
# mongosh "mongodb+srv://f1analytics.gspkb73.mongodb.net/" --apiVersion 1 --username natequan

MONGO_URI = "mongodb+srv://natequan:KlyW0bJBjQfa3Xqb@f1analytics.gspkb73.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "f1Analytics"
COLLECTION_NAME = "DriverStandings"

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

# connects to Ergast API to get driver standings data
ergast = Ergast()

# function to load a year's driver standings
def load_driver_standings(year):
    # get the driver standings data
    standings = ergast.get_driver_standings(season = year).content[0]
    # since there's no year field, include that
    standings["year"] = year
    # insert the data into the database
    collection.insert_many(standings.to_dict(orient="records"))

# function to delete the current schedule data in mongo
def delete_driver_standings():
    collection.delete_many({})

def update_driver_standings(collection):
    # gets the current standings
    current_standings = ergast.get_driver_standings(season = "current").content[0]
    # gets the current year
    current_year = datetime.now().year

    # query the max year in the database
        # groups all the records into one group and takes the max year
    result = collection.aggregate([
        {
            "$group": {
                "_id": None,
                "max_year": {"$max": "$year"}
            }
        }
    ])
    # gets the max_year
    for document in result:
        max_year = document.get("max_year", 0)

    db_standings = list(collection.find({ "year": max_year }))

    for i, row in current_standings.iterrows():
        db_row = db_standings[i]
        
        # if the two max_points values aren't equal:
            # 1 - Current year standings need to be updated
            # 2 - It's changing from last year to the current year
        if db_row["points"] != row["points"]:
            # Case 1: deletes all of this years values and updates them
            if (current_year == max_year):
                collection.delete_many( { "year": int(max_year)} )
                collection.insert_many(current_standings)
            # Case 2: keeps all of the max year's values, adds the current year standings
            else: 
                current_standings["year"] = current_year
                collection.insert_many(current_standings.to_dict(orient="records"))
            
            break

# delete_driver_standings()

# for year in range(2018, 2024):
#     load_driver_standings(year)
# load_driver_standings(2024)
# update_driver_standings()

client.close()