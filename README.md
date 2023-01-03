# yt_chat_arranger
A simple program that goes through all of previous streams and collect data. (publicly avaialbe data)

Upon starting this will ask you for channel ID. 
If you don't know how to get a channel ID. Considering how hard it have become. (https://stackoverflow.com/a/72724501/12084450)[This] should help.

Depends on how big your channel is. this can take some time. 

Extra Feature. 
you can host this and use bots like NightBot to get some data out of it. 
How ? 
you modify `api.py` file to change the "secret_key". make sure you don't leak it to anyone.
lets say secret_key is pass123
next step add a command to nightbot
`!addcom !stats $(urlfetch http://{where_you_hosting_it}/stats/$(channelid)/$(userid))`

Since this is now something that you may want to update now and then 
Add a cron job 
