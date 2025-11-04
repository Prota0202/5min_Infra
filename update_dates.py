from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/?replicaSet=rs0&readPreference=primary")
client = MongoClient(MONGO_URI)
db = client["projet2025"]
collection = db["scores"]

# Ajouter la date du jour aux documents existants qui n'ont pas encore de date
today = datetime.utcnow()
result = collection.update_many(
    {"date": {"$exists": False}},
    {"$set": {"date": today}}
)

print(f"Documents modifiés : {result.modified_count}")