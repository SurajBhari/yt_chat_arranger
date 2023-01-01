
from flask import Flask, request
from json import load
app = Flask(__name__)
from os import listdir
    

secret_key = "pass123"

@app.get('/stats/<channel_id>/<user_id>')
def stats(channel_id, user_id):
    password = ""
    try:
        password = request.headers['secret_key']
    except KeyError:
        password = ""
    if password != secret_key:
        return "INVALID KEY"
    with open(f"./{channel_id}/first_ever.json", mode="r", encoding="utf-8") as f:
        data = load(f)
    try:
        user = data[user_id]
    except KeyError:
        return "No Data Found."
    with open(f"./{channel_id}/person_wise/{user_id}.txt", mode="r", encoding="utf-8") as f:
        count = len(f.readlines())
    return f"{user['name']} You have made {count} messages, You First interacted with us on a stream that was {user['ago']}, here -> {user['link']}"

app.run(port=5012)