from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "9c1e2b7ab7631f7a84b9e1a5f48c6d3e2f6d4c3b2a1f8e9d1c0b9a8e7f6d5c4b"  # Mets ta propre clé secrète !

POD = os.getenv("HOSTNAME", "unknown")

#client = MongoClient("mongodb://mongodb.dev.svc.cluster.local:27017/?replicaSet=rs0")
#client = MongoClient("mongodb://mongodb.dev.svc.cluster.local:27017/?replicaSet=rs0")

#MONGO_URI = os.getenv(
#   "MONGO_URI",
#   "mongodb://mongodb-0.mongodb.dev.svc.cluster.local:27017,"
#   "mongodb-1.mongodb.dev.svc.cluster.local:27017,"
#   "mongodb-2.mongodb.dev.svc.cluster.local:27017"
#   "/?replicaSet=rs0"
#)
MONGO_URI = "mongodb://mongodb:27017/?replicaSet=rs0&readPreference=primary"


client = MongoClient(MONGO_URI)
db = client["projet2025"]
collection = db["scores"]

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pseudo = request.form.get("pseudo", "").strip()
        if pseudo:
            session["username"] = pseudo
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/")
def home():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))
    return render_template("index.html", username=username)

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

@app.get("/whoami")
def whoami():
    return jsonify(pod=POD)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)