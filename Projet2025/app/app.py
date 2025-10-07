from flask import Flask, render_template, jsonify, request
import os
from pymongo import MongoClient

app = Flask(__name__)

POD = os.getenv("HOSTNAME", "unknown")

# Connexion à MongoDB ReplicaSet (adapte l'URI si besoin)
client = MongoClient("mongodb://mongodb.dev.svc.cluster.local:27017/?replicaSet=rs0")
db = client["projet2025"]
collection = db["scores"]

@app.get("/whoami")
def whoami():
    return jsonify(pod=POD)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scores")
def scores():
    all_scores = collection.find()
    scores_list = [{"nom": score.get("nom", ""), "score": score.get("score", "")} for score in all_scores]
    return render_template("scores.html", scores=scores_list)

@app.route("/api/score", methods=["POST"])
def api_score():
    data = request.get_json()
    nom = data.get("nom")
    score = data.get("score")
    if nom and score is not None:
        collection.update_one(
            {"nom": nom},
            {"$set": {"score": score}},
            upsert=True
        )
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Missing nom or score"}), 400

if __name__ == "__main__":
    app.run(debug=True)