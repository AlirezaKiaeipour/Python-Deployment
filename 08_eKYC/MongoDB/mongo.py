from pymongo import MongoClient
from fastapi import FastAPI

app = FastAPI()

client = MongoClient("mongodb://mongodb:27017/")
db = client.ekyc_db