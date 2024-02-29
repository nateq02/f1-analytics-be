from pymongo.mongo_client import MongoClient
from pymongo import UpdateMany
import fastf1 as f1
from datetime import datetime
import pandas as pd
import numpy as np
import time as time

# for running in shell
# mongosh "mongodb+srv://f1analytics.gspkb73.mongodb.net/" --apiVersion 1 --username natequan

MONGO_URI = "mongodb+srv://natequan:KlyW0bJBjQfa3Xqb@f1analytics.gspkb73.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "f1Analytics"
COLLECTION_NAME = "Events"

# Create a new client and connect to the server
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# disabling cache created by the f1 library
    # loading session data takes up a lot of storage in the cache
# f1.Cache.clear_cache()
# f1.Cache.set_disabled()

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# function to load a given year's schedule
def load_events(year):
    # loads the schedule from Fastf1
    schedule = f1.get_event_schedule(year)

    # creates a condition to eliminate testing events
    condition = (schedule['RoundNumber'] == 0)
    schedule = schedule[~condition]

    # columns of a schedule event where a value could be NaT, which causes errors
    time_columns = [
                        "EventDate",
                        "Session1Date",
                        "Session1DateUtc",
                        "Session2Date",
                        "Session2DateUtc",
                        "Session3Date",
                        "Session3DateUtc",
                        "Session4Date",
                        "Session4DateUtc",
                        "Session5Date",
                        "Session5DateUtc"
                    ]
    
    # sets all NaT values in the column array to none to avoid errors
    for col in time_columns:
        schedule[col] = schedule[col].replace({pd.NaT: None})
    
    # converts the schedule object to a dictionary
    schedule_dict = schedule.to_dict(orient="records")

    # for each event in the schedule, we want to get the results for that event
    for record in range(len(schedule_dict)):
        # # try to load the session data for the given event
        #     # specifically, we want data for the race and qualifying sessions for each event
        try:
            qual = f1.get_session(year=int(schedule_dict[record]["EventDate"].year), gp=schedule_dict[record]["RoundNumber"], identifier='Qualifying')
            qual.load()

            race = f1.get_session(year=int(schedule_dict[record]["EventDate"].year), gp=schedule_dict[record]["RoundNumber"], identifier='Race')
            race.load()

        except Exception as e:
            break
        
        # within a session object, we only want the results table
        qual_result = qual.results
        race_result = race.results

        # drop unnecessary columns to reduce the amount of data being stored
        qual_result = qual_result.drop(columns = ["BroadcastName", "DriverId", "TeamColor", "TeamId", "HeadshotUrl", 
                                    "ClassifiedPosition", "GridPosition", "Time", "Status", "Points"])

        race_result = race_result.drop(columns = ["BroadcastName", "DriverId", "TeamColor", "TeamId", "HeadshotUrl",
                                    "Q1", "Q2", "Q3"])

        # Handling the time columns in the qual results
        for col in ["Q1", "Q2", "Q3"]: 
            # mongo can't encode TimeDelta values, so they must be converted
            qual_result[col] = qual_result[col].dt.total_seconds()
            # must handle NaN values to avoid errors
            qual_result[col] = qual_result[col].replace({np.nan: None})
        
        qual_result["Position"] = qual_result["Position"].replace({np.nan: None})

        # As above, handling TimeDelta values and NaN values
        race_result["Time"] = race_result["Time"].dt.total_seconds()
        race_result["Time"] = race_result["Time"].replace({np.nan: None})
        race_result["Position"] = race_result["Position"].replace({np.nan: None})
        race_result["GridPosition"] = race_result["GridPosition"].replace({np.nan: None})
        race_result["Points"] = race_result["Points"].replace({np.nan: None})

        # converting the results tables into dictionaries so they can be nested into the events dictionary
        schedule_dict[record]["QualifyingResult"] = qual_result.to_dict(orient="records")
        schedule_dict[record]["RaceResult"] = race_result.to_dict(orient="records")

        # checking if an event is a sprint weekend to get those results as well
        if schedule_dict[record]["EventFormat"] == "sprint" or schedule_dict[record]["EventFormat"] == "sprint_shootout": 
            # As above, we want to use try/except if the to see if the session has actually occurred yet
            try:
                sprint = f1.get_session(year=int(schedule_dict[record]["EventDate"].year), gp=schedule_dict[record]["RoundNumber"], identifier='Sprint')
                sprint.load()

                # sprint and sprint_shootouts are handled differently
                    # with sprint_shootouts (post 2023), want to show the shootout results in addition to the sprint
                    # sprints prior to 2023 do not have this separate session
                if schedule_dict[record]["EventFormat"] == "sprint_shootout":
                    sprint_shootout = f1.get_session(year=int(schedule_dict[record]["EventDate"].year), gp=schedule_dict[record]["RoundNumber"], identifier='Sprint Shootout')
                    sprint_shootout.load()

            # if loading the session produces an error, the event has not happened yet
            except Exception as e:
                print(e)
                break
            
            # handle the sprint results the same as the race_results above
            sprint_result = sprint.results
            sprint_result = sprint_result.drop(columns = ["BroadcastName", "DriverId", "TeamColor", "TeamId", "HeadshotUrl",
                                        "Q1", "Q2", "Q3"])
            
            sprint_result["Time"] = sprint_result["Time"].dt.total_seconds()
            sprint_result["Time"] = sprint_result["Time"].replace({np.nan: None})
            sprint_result["Position"] = sprint_result["Position"].replace({np.nan: None})
            sprint_result["GridPosition"] = sprint_result["GridPosition"].replace({np.nan: None})
            sprint_result["Points"] = sprint_result["Points"].replace({np.nan: None})

            schedule_dict[record]["SprintResult"] = sprint_result.to_dict(orient="records")
            # handle the sprint shootout results the same as qualifying_results above
            if schedule_dict[record]["EventFormat"] == "sprint_shootout":
                sprint_shootout_result = sprint_shootout.results
                sprint_shootout_result = sprint_shootout_result.drop(columns = ["BroadcastName", "DriverId", "TeamColor", "TeamId", "HeadshotUrl", 
                                    "ClassifiedPosition", "GridPosition", "Time", "Status", "Points"])
                
                for col in ["Q1", "Q2", "Q3"]: 
                    sprint_shootout_result[col] = sprint_shootout_result[col].dt.total_seconds()
                    sprint_shootout_result[col] = sprint_shootout_result[col].replace({np.nan: None})
                
                sprint_shootout_result["Position"] = sprint_shootout_result["Position"].replace({np.nan: None})

                schedule_dict[record]["SprintShootoutResult"] = sprint_shootout_result.to_dict(orient="records")

    # insert the schedule to the database without testing events
    collection.insert_many(schedule_dict)

# function to delete the current schedule data in mongo
def delete_events():
    collection.delete_many({})

# function to update the schedule
def update_events():
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
        load_events(current_year)
    
    # if max_year = current year, check if next year's data is available (not empty)
        # if so, upload that too
    else:
        next_year_schedule = f1.get_event_schedule(current_year+1)
        if not next_year_schedule.empty:
            load_events(current_year + 1)


# delete_events()
# for year in range(2018, 2024):
#     load_events(year)
update_events()
# load_events(2018)
# load_events(2019)
# load_events(2020)
# load_events(2021)
# load_events(2022)
# load_events(2023)

client.close()