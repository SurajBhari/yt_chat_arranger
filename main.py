from chat_downloader import ChatDownloader, errors
import scrapetube

from datetime import datetime
from os import listdir, mkdir
import json

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--Channel", help="Channel ID")
args = parser.parse_args()
if not args.Channel:
    channel_id = str(input("Enter Channel ID"))

errorss = ""


videos = scrapetube.get_channel(channel_id, content_type="streams")

titles = []
vids = []
first_ever_message = {}  #
count = 1
for video in videos:
    vids.append(video)
    title = video["title"]["runs"][0]["text"]
    titles.append(title)
    print(count, end=" ")
    count += 1

if channel_id not in listdir("."):
    mkdir(channel_id)
    mkdir(f"{channel_id}/json_storage")
    mkdir(f"{channel_id}/chats_storage")
    mkdir(f"{channel_id}/person_wise")


with open(f"{channel_id}/titles.txt", "w+", encoding="utf-8") as f:
    f.write("\n".join(titles))

total_chats = []
for video in vids[::-1]:
    id = video["videoId"]
    try:
        print(
            f"processing a stream that was {video['publishedTimeText']['simpleText']}"
        )
    except KeyError:
        continue
    try:
        if "watching" in video["viewCountText"]["runs"][1]["text"]:
            print("Skipping {id} cuz it's currently getting streamed")
            continue
    except KeyError:
        pass
    if id + ".json" in listdir(f"./{channel_id}/json_storage"):
        try:
            chat = json.load(
                open(
                    f"./{channel_id}/json_storage/" + id + ".json",
                    "r",
                    encoding="utf-8",
                )
            )["messages"]
            print("loaded from local storage")
        except json.decoder.JSONDecodeError:
            print("error decoding the mssage. so getting out of here.")
            continue
    else:
        try:
            chat = ChatDownloader().get_chat(video["videoId"])
        except errors.NoChatReplay:
            continue
    string = ""
    messages = {"messages": []}
    for message in chat:
        message["vid"] = id
        total_chats.append(message)
        # since we reversed the order of videos processed we can do in check
        if message["author"]["id"] not in first_ever_message.keys():
            first_ever_message[message["author"]["id"]] = {
                "name": message["author"]["name"],
                "video_id": id,
                "timestamp": message["time_in_seconds"],
                "link": f"https://youtu.be/{id}?t={int(message['time_in_seconds'])}",  # we learn a lot of stuff. one of those is yt don't like float
                "message": message["message"],
                "ago": video["publishedTimeText"]["simpleText"],
            }
        time = datetime.fromtimestamp(int(message["timestamp"]) / 1000000).strftime(
            "%d/%m/%Y, %H:%M:%S"
        )
        try:
            string += f"{time} | {message['time_in_seconds']} | https://youtu.be/{id}?t={int(message['time_in_seconds'])} | {message['time_text']} | {message['author']['name']} | {message['message']}\n"
            messages["messages"].append(message)
        except Exception as e:
            print(e)
            errorss += f"{id} | {e}\n"

    with open(f"./{channel_id}/chats_storage/{id}.txt", "w+", encoding="utf-8") as f:
        f.write(string)

    with open(f"./{channel_id}/json_storage/{id}.json", "w+", encoding="utf-8") as f:
        json.dump(messages, f, indent=4)


# Now lets get all of the chats in one dictionary to save some time and all


with open(f"./{channel_id}/first_ever.json", "w+", encoding="utf-8") as f:
    json.dump(first_ever_message, f, indent=4)
    print("made first_ever json")

print(str(len(total_chats)) + " Chats were made")

person_wise = {}
for chat in total_chats:
    try:
        person_wise[chat["author"]["id"]]
    except KeyError:
        person_wise[chat["author"]["id"]] = {
            "name": chat["author"]["name"],
            "count": 0,
            "messages": [],
        }

    person_wise[chat["author"]["id"]]["count"] += 1
    person_wise[chat["author"]["id"]]["name"] = chat["author"]["name"]
    time = datetime.fromtimestamp(int(message["timestamp"]) / 1000000).strftime(
        "%d/%m/%Y, %H:%M:%S"
    )
    person_wise[chat["author"]["id"]]["messages"].append(
        f"{time} | https://youtu.be/{message['vid']}?t={int(chat['time_in_seconds'])} | {chat['time_text']} | {chat['author']['name']} | {chat['message']}"
    )


a = dict(sorted(person_wise.items(), key=lambda item: item[1]["count"]))
b = {}
for key in reversed(a):
    b[key] = a[key]

string_to_write = ""
for item in b:
    string_to_write += f"{item} | {b[item]['count']} | {b[item]['name']}\n"

for person in person_wise:
    try:
        with open(
            f"./{channel_id}/person_wise/{person}.txt", "w+", encoding="utf-8"
        ) as f:
            f.write("\n".join(b[person]["messages"]))
    except Exception as e:
        print(f"fuck no weirdo name {e}")
with open(f"./{channel_id}/person_wise.txt", "w+", encoding="utf-8") as f:
    f.write(string_to_write)
