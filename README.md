# VATSIM-Discord-Bot
## VATSIM Discord Bot is developed by VATSIM Adria members with a goal of displaying VATSIM related data on Discord server. With this version our bot got smarter, better and more powerfull in features that were once only a dream for us. When our first bot was released it was just a dumb python script with 700+ lines of unorganized mess in code and now it took form of standard Discord bot made for 21st century. 

## Features
Since we started this project long ago we made huge improvements on how does bot respond to commands and what it can do. In last period we dedicated time to optimize the code, make it easier to use and implemented a bunch of different commands for members, staff and Admins to use. 
Here is short list of what this bot can do:
*Display arrivals and departures from one or all airports under your vACC/ARTCC
*Automatic ATC Bookings and Online announcements
*Decoded METAR
*Broadcast commands (news, events, sector file updates, and push to be used for messaged related to event)
*Display online controllers on command
*load/unload/reload cogs (Only usable by admins)
*Paginated Help page to show commands and their info


## Modifying bot
As this is bot that you will need to host on your own you don't need to have extensive Python knowledge to make it work as it should. We implemented config files which can be used for most parts of bot edit but you will also have to edit 4 python files with correct data so bot can perform calculations of ETA. You can use Visual Studio Code or Notepad ++ (or any code editor you like) to edit this files just make sure to follow examples left in files.

So let's see what we need to edit:
*Under bot_config you have 2 files to edit: secrets.json and config.json. First let's start with secrets.json where you need to enter your bot token from Discord Developer Portal. Once you done that let's move to config.json file. Here you will need to enter channel ID's (you can get them by right clicking on text channel and selecting Copy ID). This ID's are used in code for annoucements and broadcasts so make sure to select correct channels for bot to send messages to. 
*airports.json - enter all ICAO codes for airports in your vACC/ARTCC. This is used for departure and arrival commands to display correct data,
*callsign_prefix - enter all airport and CTR codes under your vACC/ARTCC. You can simply copy content from airports.json and add CTR & FSS stations,
*To make sure bot can make ETA calculations you will have to edit 4 files which looks for coordinates of the airports. Navigate to cogs folder and find allArrivals.py, arrivals.py, allDepartures.py and departures.py (you can combine departures and arrivals by simply copy/paste code from one file to another without imports and class) and find airport coordinates located in code. You will have to enter all airport coordinates in order to bot to correctly calculate ETA times and determine status of the flight. 
 

## Example
You want to find out how does this bot work on day-to-day basis? Fear not simply hop into our Discord server at: https://discord.gg/nsBQcdY link your VATSIM & Discord Accounts and you will be able to use this bot made for VATSIM Adria to explore all functions of the bot. Also, you can get support by developer (find him under as Marko Tomicic - 1359931 on our Discord).


## How to host the bot?
In order to host this bot you have 2 options (let's assume you want it to run 24/7):
1.) Host it on VPS such as DO,
2.) Host it on some old laptop, Raspbery Pi, etc

While both of this options will work just fine I would recommend getting VPS from DO (Droplet) which will cost you around 5$ a month for basic Ubuntu based server. Also there is docummentation available on their site on how to host it and you don't need to worry about up time, shortages or anything as it is hosted outside of your home. Also make sure to install all required frameworks (Discord & Buttons) in order for code to work. They can be found in requirements.txt so you can simply run pip install -r requirements.txt and it will download and install all needed frameworks
