# yt_chat_arranger

Archived because of newer better version [here](https://github.com/SurajBhari/yt_stats_api)
A simple program that goes through all of previous streams and collect data. (publicly avaialbe data)

Upon starting this will ask you for channel ID. 
If you don't know how to get a channel ID. Considering how hard it have become. [This](https://stackoverflow.com/a/72724501/12084450) should help.

Depends on how big your channel is. this can take some time. 

Extra Feature. 
you can host this and use bots like NightBot to get some data out of it. 
How ? 
next step add a command to nightbot
`!addcom !stats $(urlfetch http://{where_you_hosting_it}/stats/)`

Since this is now something that you may want to update now and then 
Add a cron job 
`0 0 * * *  cd /root/yt_chat_arranger && python3 main.py {channel_id_here}`
this run at every 12 in night.
