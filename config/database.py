# A file to store database information

from pymongo import MongoClient
from datetime import datetime
MONGO_URI = "mongodb+srv://natequan:KlyW0bJBjQfa3Xqb@f1analytics.gspkb73.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "f1Analytics"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# collection = db["Events"]

# def get_events(year):
#     start_date = datetime(2018, 1, 1)
#     now = datetime.now()
#     # query events that come after "now"
#     query = collection.find({"EventDate": {"$lt": now}})#.sort("RoundNumber", 1)
#     print(list(query))

# get_events(2023)