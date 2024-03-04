from config.database import db
from datetime import datetime

COLLECTION_NAME = "Events"

collection = db[COLLECTION_NAME]

def get_events(year):
    start_date = datetime(2018, 1, 1)
    now = datetime.now()
    # query events that come after "now"
    query = collection.find({"EventDate": {"$gt": now}})#.sort("RoundNumber", 1)
    print(query)