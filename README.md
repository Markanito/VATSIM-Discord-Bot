# VATSIM-Discord-Bot
## Discord bot to display online ATC, departures, arrivals and future bookings!


## Requirements
In order to modify this bot to suit your needs (it won't work out of box) you will need:
* Visual Studio Code (VCS)
* Discord.py
* Requests
* ElementTree
* Asyncio

## Modifying bot
In VCS you will need to make some changes so bot can filter VATSIM Data for your needs. You will need following data:
* ATC station ICAO (include all stations and prefixes such as XXXX_U_CTR, XXXX_SC_CTR, etc)
* ICAO code for airports within FIR or vACC
* Coordinates of airports (this is for calculation of ETA)
* Discord bot token (you can find how to make bot simply by googling it)

## Example
If you want to take a look of fully working bot, you can join our Discord server here: https://discord.gg/nsBQcdY

If you have any questions feel free to contact me via email: marko.tomicic@vatadria.net or via Discord: Markan#4169

## How to host the bot for free?
I included proc and requirements files so you can host this bot without problems. Heroku offers free hosting for this bot so head over to: https://heroku.com/ and sign up (it is 100% free but there is payed versions as well for more functions). 
There is tutorial on how to deploy your bot on heroku there it should take 10 min max for the first time setup.

Happy coding and enjoy our bot. 

P.S. Expect future updates to code once when other functions get implemented.
List of futre plans:
- Automatic messages when ATC station goes online or offline
- Filtering arrival and departure data by ICAO
- Implementing METAR command (decoded and undecoded data will be provided)

Keep an eye on future code updates in order to stay up to date. If you make any changes that you would like to share it with the world feel free to reach out to me.
