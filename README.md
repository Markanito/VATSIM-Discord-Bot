# VATSIM-Discord-Bot
## VATSIM Discord bot which is designed for VATSIM-Adria Discord server is now available for every vACC to use. Down bellow you have a list of features you can use so please make sure to follow it as written bellow. This bot will be updated for an easier setup but I decided to share this new version with everyone to modify and use.


## Requirements
In order to modify this bot to suit your needs (it won't work out of box) you will need:
* Visual Studio Code (VCS)
* Discord.py
* Requests
* ElementTree
* Asyncio

## Features
Since we started this project long ago we made huge improvements on how does bot perform and it is not stupid script anymore it is much more than that. Here are some of the features that this bot can do (more to come in future)
*Display arrivals and departures from one or all airports under your vACC/ARTCC
*Automatic ATC Bookings and Online announcements
*Decoded METAR
*Broadcast commands (news, events, sector file updates, and push to be used for messaged related to event)
*Display online controllers on command
*load/unload/reload cogs (Only usable by admins)
*Paginated Help page to show commands and their info


## Modifying bot
You will need to modify the bot code a bit until config file is published and implemented. You can also remove unneeded cogs from cogs folder but before you do make sure to check what is there and will you need that.
So let's see what we need to edit:
*airports.json - enter all ICAO codes for airports in your vACC/ARTCC. This is used for departure and arrival commands to display correct data,
* callsign_prefix - enter all airport and CTR codes under your vACC/ARTCC. You can simply copy content from airports.json and add CTR & FSS stations,
* Under cogs folder you will have to modify 4 files allArrivals.py, arrivals.py, allDepartures.py and departures.py with airport coordinates in order to perform correct ETA calculations. For METAR command to work you will need to edit metar.py and insert your checkwx API key. CheckWX is free up to 2000 requests per day so it will be more then enough for your server. If you desire to use any other METAR provider you will have to rework entire metar.py as it is built for CheckWX API. 
* Under bot_config->secrets you will have to enter you Discord Bot token found under Discord Developer portal


## Example
If you want to take a look at how does this bot works on server you can join VATAdria server at: https://discord.gg/nsBQcdY. Keep in mind you will have to link your VATSIM & Discord Accounts in order to access the server. If you have any further questions you can send me a message (Marko Tomicic - 1359931 on Discord server) and I will gladly assist with any questions.


## How to host the bot?
While with v1 you could use heroku to host it, with this version you will not be albe to do so and I suggest using DigitalOcean which will cost you around 5$ per month to keep the bot up and running 24/7. If you need help there are documentation on DO site or you can again contact me via Discord and I will be happy to help. 


