
from flask import Flask, request
from json import load
app = Flask(__name__)
from os import listdir

import json
from urllib.parse import parse_qs


    
@app.get("/")
def main():
    return "hello world"

@app.get('/stats/')
def stats():
    try:
        channel = parse_qs(request.headers["Nightbot-Channel"])
        user = parse_qs(request.headers["Nightbot-User"])
    except KeyError:
        return "Not able to auth"

    channel_id = channel.get("providerId")[0]
    user_id = user.get("providerId")[0]

    if channel_id not in listdir("."):
        return "Channel not cached (yet)"
    with open(f"./{channel_id}/first_ever.json", mode="r", encoding="utf-8") as f:
        data = load(f)
    with open(f"./{channel_id}/person_wise/{user_id}.txt", mode="r", encoding="utf-8") as f:
        count = len(f.readlines())
    print("Here")
    user_data = data[user_id]
    print(user_data)
    return f"{user_data['name']} You have made {count} messages, You First interacted with us on a stream that was {user_data['ago']}, here -> {user_data['link']}"

app.run(port=5000, host="0.0.0.0")
