from pymongo.mongo_client import MongoClient
from config import *

client = MongoClient(MONGO_CLIENT_STRING)
db = client.Sync