from chat_downloader import ChatDownloader, errors
import scrapetube

from os import listdir
import json

errorss = ''
channel_id = str(input("Enter Channel ID"))


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
    
    try:
        if 'watching' in video['viewCountText']['runs'][1]['text']:
            print("Skipping {id} cuz it's currently getting streamed")
            continue
    except KeyError:
        pass

    if id + '.json' in listdir("./json_storage"):
        chat = json.load(open("./json_storage/"+id+'.json', 'r'))['messages']
        print("Json Format for the video already exists. Not downloading")
    else:
        try:
            chat = ChatDownloader().get_chat(video['videoId'])
        except errors.NoChatReplay:
            continue
    string = ""
    messages = {'messages':[]}
    try: 
        for message in chat:
            try:
                print(message['message'])
                string += f"{message['timestamp']} | {message['time_in_seconds']} | {message['time_text']} | {message['author']['name']} | {message['message']}\n"
                messages['messages'].append(message)
            except Exception as e:
                print(e)
                errorss += f"{id} | {e}\n"
    except Exception as e:
        errorss += f"{id} | {e}\n"
        print(errorss)
        continue


    with open(f'chats_storage/{id}.txt', "w+", encoding='utf-8') as f:
        f.write(string)
    
    with open(f'json_storage/{id}.json', "w+", encoding='utf-8') as f:
        json.dump(messages, f, indent=4)
    

#Now lets get all of the chats in one dictionary to save some time and all

chats = []

for filename in listdir("./json_storage"):
    if filename.endswith(".json"):
        data = json.load(open("./json_storage/"+filename, 'r'))
        chats.extend(data['messages'])

print(len(chats) + " Chats were made")

person_wise = {}
for chat in chats:
    try:
        person_wise[chat['author']['id']]
    except KeyError:
        person_wise[chat['author']['id']] = {'name': chat['author']['name'], 'count': 0, 'messages':[]}
    
    person_wise[chat['author']['id']]['count'] += 1
    person_wise[chat['author']['id']]['name'] = chat['author']['name']


a = dict(sorted(person_wise.items(), key=lambda item: item[1]["count"]))
b = {}
for key in reversed(a):
    b[key] = a[key]

string_to_write = ""
for item in b:
    string_to_write += f"{item} | {b[item]['count']} | {b[item]['name']}\n"

with open("person_wise.txt", "w+", encoding='utf-8') as f:
    f.write(string_to_write)
