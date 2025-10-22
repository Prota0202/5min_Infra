from pymongo import MongoClient

client = MongoClient(
    'mongodb://mongodb-0.mongodb.dev.svc.cluster.local:27017,'
    'mongodb-1.mongodb.dev.svc.cluster.local:27017,'
    'mongodb-2.mongodb.dev.svc.cluster.local:27017/?replicaSet=rs0'
)

db = client['projet2025']
collection = db['scores']

# Insérer des scores test
initial_scores = [
    {'nom': 'Alice', 'score': 50},
    {'nom': 'Bob', 'score': 75},
    {'nom': 'Charlie', 'score': 30}
]

for score in initial_scores:
    collection.update_one(
        {'nom': score['nom']},
        {'$set': {'score': score['score']}},
        upsert=True
    )

print(list(collection.find()))
