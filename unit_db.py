from pymongo import MongoClient

# Connexion locale à MongoDB
client = MongoClient("mongodb://localhost:27017/")
# Création de la base de données et de la collection
db = client["projet2025"]
collection = db["scores"]

# Données exemples
sample_data = [
    {"nom": "Alice", "score": 1200},
    {"nom": "Bob", "score": 950},
    {"nom": "Charlie", "score": 1450}
]

# Nettoyage avant insertion (optionnel)
collection.delete_many({})

# Insertion des données
collection.insert_many(sample_data)

print("✅ Base de données 'projet2025' et collection 'scores' créées avec succès !")
print("👉 Données d'exemple ajoutées :", sample_data)
