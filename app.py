from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend to fetch data

# MongoDB Connection (Change URI if using MongoDB Atlas)
client = MongoClient("mongodb://localhost:27017")
db = client.github_events
events_collection = db.events

@app.route("/webhook", methods=["POST"])
def github_webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    timestamp = datetime.utcnow().strftime("%d %b %Y - %I:%M %p UTC")

    if event_type == "push":
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        message = f"{author} pushed to {to_branch} on {timestamp}"

    elif event_type == "pull_request":
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        message = f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"

    elif event_type == "merge":  # Optional: Handle merge events
        author = data['sender']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        message = f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"

    else:
        return jsonify({"status": "ignored"}), 200

    # Save event to MongoDB
    events_collection.insert_one({
        "event_type": event_type,
        "message": message,
        "timestamp": timestamp
    })

    print("Saved event:", message)
    return jsonify({"status": "success"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    events = list(events_collection.find({}, {"_id": 0}))
    return jsonify(events)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
