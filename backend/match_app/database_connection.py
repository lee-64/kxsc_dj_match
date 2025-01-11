from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


def get_db():
    client = MongoClient(os.getenv('MONGO_CONNECTION_URI'))
    return client
