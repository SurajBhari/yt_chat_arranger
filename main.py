from chat_downloader import ChatDownloader, errors
import scrapetube

from os import listdir
import json

channel_id = 'UCIzzPhdRf8Olo3WjiexcZSw'
#channel_id = str(input("Enter Channel ID"))


videos = scrapetube.get_channel(channel_id)

vids = []
for video in videos:
    vids.append(video)
    print("{}".format(video['title']['runs'][0]['text']))

for video in vids:
    id = video['videoId']
    if id+".txt" in listdir("./chats_storage"):
        if id+'.json' in listdir("./json_storage"):
            print(f"Skipping {id} cuz it already exists")
            continue
    if id + '.json' in listdir("./json_storage"):
        chat = json.load(open("./json_storage/"+id+'.json', 'r'))['messages']
    else:
        try:
            chat = ChatDownloader().get_chat(video['videoId'])
        except errors.NoChatReplay:
            continue
    string = ""
    messages = {'messages':[]}
    for message in chat:
        try:
            print(message['message'])
            string += f"{message['timestamp']} | {message['time_in_seconds']} | {message['time_text']} | {message['author']['name']} | {message['message']}\n"
            messages['messages'].append(message)
        except Exception as e:
            print(e)

    with open(f'chats_storage/{id}.txt', "w+", encoding='utf-8') as f:
        f.write(string)
    
    with open(f'json_storage/{id}.json', "w+", encoding='utf-8') as f:
        json.dump(messages, f, indent=4)
    
        
