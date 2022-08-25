from chat_downloader import ChatDownloader, errors
import scrapetube

from os import listdir

channel_id = 'UCIzzPhdRf8Olo3WjiexcZSw'
#channel_id = str(input("Enter Channel ID"))


videos = scrapetube.get_channel(channel_id)

for video in videos:
    id = video['videoId']
    if id+".txt" in listdir("./chats_storage"):
        print(f"Skipping {id} cuz it already exists")
        continue
    print(f"Looking at video id - {video['videoId']}")
    try:
        chat = ChatDownloader().get_chat(video['videoId'])
    except errors.NoChatReplay:
        continue
    string = ""
    for message in chat:
        try:
            print(message['message'])
            string += f"{message['timestamp']} | {message['time_in_seconds']} | {message['time_text']} | {message['author']['name']} | {message['message']}\n"
        except Exception as e:
            print(e)

    with open(f'chats_storage/{id}.txt', "w+", encoding='utf-8') as f:
        f.write(string)
        
