from pymongo import MongoClient
from os import environ
from dotenv import load_dotenv

load_dotenv()
mongo_url = environ.get("mongo_db_url")

client = MongoClient(mongo_url)
db = client["zhunehra"]
users_collection = db["users"]
groups_collection = db["groups"]
