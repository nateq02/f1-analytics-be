from pymongo.mongo_client import MongoClient
import fastf1 as f1
from datetime import datetime
import pandas as pd

# for running in shell
# mongosh "mongodb+srv://f1analytics.gspkb73.mongodb.net/" --apiVersion 1 --username natequan

MONGO_URI = "mongodb+srv://natequan:KlyW0bJBjQfa3Xqb@f1analytics.gspkb73.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "f1Analytics"
COLLECTION_NAME = "F1Events"

# Create a new client and connect to the server
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# function to load a given year's schedule
def load_schedule(year):
    # loads the schedule from Fastf1
    schedule = f1.get_event_schedule(year)

    # creates a condition to eliminate testing events
    condition = (schedule['RoundNumber'] == 0)
    schedule = schedule[~condition]

    # insert the schedule to the database without testing events
    collection.insert_many(schedule.to_dict(orient="records"))

# function to load 2020's schedule - one of the records has NaT records, which impacts the datetime datatype
def load_2020_schedule():
    schedule = f1.get_event_schedule(2020)
    condition = (schedule['RoundNumber'] == 0)
    schedule = schedule[~condition]

    # replacing the NaT records with None
    schedule['Session2Date'] = schedule['Session2Date'].replace({pd.NaT: None})
    schedule['Session2DateUtc'] = schedule['Session2Date'].replace({pd.NaT: None})
    schedule['Session3Date'] = schedule['Session2Date'].replace({pd.NaT: None})
    schedule['Session3DateUtc'] = schedule['Session2Date'].replace({pd.NaT: None})

    # upload to the collection as a dictionary
    collection.insert_many(schedule.to_dict(orient="records"))

# function to delete the current schedule data in mongo
def delete_schedule():
    collection.delete_many({})

# function to update the schedule
def update_schedule():
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

    # gets current year
    current_year = datetime.now().year

    # get the max year from the result collection
        # this collection should only have one result
    for document in result: 
        max_year = document.get("max_year", 0)

    # if the max year in the database is less than the current year, then update the data
    if (max_year < current_year):
        load_schedule(current_year)
    
    # if max_year = current year, check if next year's data is available (not empty)
        # if so, upload that too
    else:
        next_year_schedule = f1.get_event_schedule(current_year+1)
        if not next_year_schedule.empty:
            load_schedule(current_year + 1)


# delete_schedule()
# for year in range(2010, 2024):
#     if year == 2020: 
#         load_2020_schedule()
#     else:
#         load_schedule(year)

update_schedule()
client.close()