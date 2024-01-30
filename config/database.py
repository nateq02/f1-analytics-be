# A file to store database information

from pymongo import MongoClient

MONGO_URI = "mongodb+srv://natequan:KlyW0bJBjQfa3Xqb@f1analytics.gspkb73.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "f1Analytics"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]