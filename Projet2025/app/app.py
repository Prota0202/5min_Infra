from flask import Flask, render_template, jsonify
import os
from pymongo import MongoClient  # Ajoute cet import

app = Flask(__name__)

POD = os.getenv("HOSTNAME", "unknown")

@app.get("/whoami")
def whoami():
    return jsonify(pod=POD)

# Connexion à MongoDB via Docker Compose
client = MongoClient("mongodb://mongodb:27017/")
db = client["projet2025"]            
collection = db["scores"]        

@app.route("/")
def home():
    # Exemple d'insertion d'un score
    collection.insert_one({"nom": "Prota0202", "score": 300})
    return render_template("index.html")

@app.route("/page2")
def page2():
    return render_template("page2.html")

@app.route("/scores")
def scores():
    # Récupérer tous les scores depuis MongoDB
    all_scores = collection.find()
    scores_list = [{"nom": score.get("nom", ""), "score": score.get("score", "")} for score in all_scores]
    return render_template("scores.html", scores=scores_list)

if __name__ == "__main__":
    app.run(debug=True)
    