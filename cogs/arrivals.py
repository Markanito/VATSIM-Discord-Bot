import requests
import json
import math
import discord
import utils.json_loader

from asyncio import sleep
from datetime import datetime, date, time, timezone
from discord.ext import commands
from discord import Embed, Colour
from discord import app_commands
from helpers.config import VATADR_BLUE, GUILD_ID, VATADR_RED

airports = utils.json_loader.read_json("airports")
url = "https://www.airport-data.com/api/ap_info.json?icao=" #API to obtain airport coordinates

class Arrivals(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="arrivals",
        description="Get arrivals to desired airport"
    )
    async def arrivals(
        self,
        interaction: discord.Interaction,
        airport: str,
        private: bool = False
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=private)
        if airport in airport:
            t = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
            xy = json.dumps(t)
            s = json.loads(xy)
            arrivals_exist = False

            embed = Embed(
                title=f"Arrival Table for {airport.upper()}",
                color = VATADR_RED,
            )
            for item in s['pilots']:
                if item['flight_plan'] != None:
                    if item['flight_plan']['arrival'] == (airport.upper()):
                        try:

                            arrivals_exist = True
                            #This is just a way to convert airport of BKPR to LYPR due to API differences in airport codes
                            if item['flight_plan']['arrival'] == "BKPR":
                                arrival = "LYPR"
                            else:
                                arrival = item['flight_plan']['arrival']
                                
                            airport_data_url = f"{url}{airport}"
                            api_data = requests.get(airport_data_url).json()
                            resp = json.dumps(api_data)
                            api = json.loads(resp)
                            lan = float(api['latitude'])
                            long = float(api['longitude'])

                            # calculations
                            utc = datetime.now(timezone.utc)
                            lat1 = item['latitude'] * math.pi / 180
                            lat2 = lan * math.pi / 180
                            lon1 = item['longitude'] * math.pi / 180
                            lon2 = long * math.pi / 180

                            dlat = lat2 - lat1
                            dlon = lon2 - lon1

                            R = (6371 * 1000) / 1852
                            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) * math.sin(dlon/2)

                            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

                            distance = R * c
                            callsign = item['callsign']
                            departure = item['flight_plan']['departure']
                            arrival = item['flight_plan']['arrival']
                                    
                            #ETA calculation, do not mess with this or it can cause wrong ETA calculations
                            if item['groundspeed'] > 40:
                                time = int(distance) / int(item['groundspeed'])
                                hour = int(time)
                                arrival_hour = utc.hour + hour
                                arrival_minute = utc.minute + int((time - int(time))*60)
                                arrival_time = f"{arrival_hour}:{arrival_minute}z"
                                if arrival_minute <10:
                                    arrival_time = f"{arrival_hour}:0{arrival_minute}z"

                                elif 10 < arrival_minute < 59:
                                    arrival_time = f"{arrival_hour}:{arrival_minute}z"
                                    

                                elif arrival_minute > 59:
                                    add_hour = int(arrival_minute / 60)
                                    arrival_minute = int(((arrival_minute / 60) - add_hour) * 60)
                                    arrival_hour = arrival_hour + add_hour
                                    if arrival_minute <10:
                                        arrival_time = f"{arrival_hour}:0{arrival_minute}z"

                                    else:
                                        arrival_time = f"{arrival_hour}:{arrival_minute}z"
                                else:
                                    arrival_time= f"{arrival_hour}:{arrival_minute}z"   

                                if arrival_hour > 23:
                                    days = int(arrival_hour / 24)
                                    arrival_hour = (arrival_hour - (days * 24))
                                    if days == 1:
                                        if arrival_minute < 10:
                                            arrival_time = f"{arrival_hour}:0{arrival_minute}z tomorrow"
                                        else:
                                            arrival_time = f"{arrival_hour}:{arrival_minute}z tomorrow"
                            else:
                                arrival_time = f"Unknown"

                            #Once everything is set, add fields to embed defined above and display it as a table
                            embed.add_field(
                                name=f":airplane: C/S:{' '} `{callsign}`{' '} |{' '} :airplane_departure: ADEP {' '}`{departure}`{' '}  | {' '} :airplane_arriving: ADES {' '}`{arrival}`{' '} | {' '} :clock1: ETA: {' '}`{arrival_time}`",
                                value="\uFEFF",
                                inline=False
                            )
                    #In case there is error running the code it will display traceback of that error.
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to load arrivals",
                                value=f"{e}",
                                inline=False
                            ) 
            if arrivals_exist:
                await interaction.followup.send(embed=embed)
            else:
                embed = Embed(
                    title=f"Arrivals Table for {airport.upper()}",
                    color = VATADR_RED,
                )
                embed.add_field(
                    name=f":x: No arrivals at the moment. :x:",
                    value=f"\uFEFF",
                    inline=False
                )
                await interaction.followup.send(embed=embed)

    @app_commands.command(
        name="allarrivals",
        description="Get all arrivals"
    )
    async def allarrivals(
        self,
        interaction: discord.Interaction,
        private: bool = False
    ):
        await interaction.response.defer(thinking=True, ephemeral=private)
        resp = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
        data = json.dumps(resp)
        s = json.loads(data)
        arrivals_exist = False
        embed = Embed(
            title=f"Arrival Table",
            color = VATADR_BLUE,
        )
        for item in s['pilots']:
            if item['flight_plan'] != None:
                if item['flight_plan']['arrival'] in airports:
                    try:
                        arrivals_exist = True
                        #This is just a way to convert airport of BKPR to LYPR due to API differences in airport codes
                        if item['flight_plan']['arrival'] == "BKPR":
                            arrival = "LYPR"
                        else:
                            arrival = item['flight_plan']['arrival']
                            
                        airport_data_url = f"{url}{arrival}"
                        api_data = requests.get(airport_data_url).json()
                        resp = json.dumps(api_data)
                        api = json.loads(resp)
                        lan = float(api['latitude'])
                        long = float(api['longitude'])

                        # calculations
                        utc = datetime.now(timezone.utc)
                        lat1 = item['latitude'] * math.pi / 180
                        lat2 = lan * math.pi / 180
                        lon1 = item['longitude'] * math.pi / 180
                        lon2 = long * math.pi / 180

                        dlat = lat2 - lat1
                        dlon = lon2 - lon1

                        R = (6371 * 1000) / 1852
                        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) * math.sin(dlon/2)

                        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

                        distance = R * c
                        callsign = item['callsign']
                        departure = item['flight_plan']['departure']
                        arrival = item['flight_plan']['arrival']
                                
                        #ETA calculation, do not mess with this or it can cause wrong ETA calculations
                        if item['groundspeed'] > 40:
                            time = int(distance) / int(item['groundspeed'])
                            hour = int(time)
                            arrival_hour = utc.hour + hour
                            arrival_minute = utc.minute + int((time - int(time))*60)
                            arrival_time = f"{arrival_hour}:{arrival_minute}z"
                            if arrival_minute <10:
                                arrival_time = f"{arrival_hour}:0{arrival_minute}z"

                            elif 10 < arrival_minute < 59:
                                arrival_time = f"{arrival_hour}:{arrival_minute}z"
                                

                            elif arrival_minute > 59:
                                add_hour = int(arrival_minute / 60)
                                arrival_minute = int(((arrival_minute / 60) - add_hour) * 60)
                                arrival_hour = arrival_hour + add_hour
                                if arrival_minute <10:
                                    arrival_time = f"{arrival_hour}:0{arrival_minute}z"

                                else:
                                    arrival_time = f"{arrival_hour}:{arrival_minute}z"
                            else:
                                arrival_time= f"{arrival_hour}:{arrival_minute}z"   

                            if arrival_hour > 23:
                                days = int(arrival_hour / 24)
                                arrival_hour = (arrival_hour - (days * 24))
                                if days == 1:
                                    if arrival_minute < 10:
                                        arrival_time = f"{arrival_hour}:0{arrival_minute}z tomorrow"
                                    else:
                                        arrival_time = f"{arrival_hour}:{arrival_minute}z tomorrow"
                        else:
                            arrival_time = f"Unknown"

                        #Once everything is set, add fields to embed defined above and display it as a table
                        embed.add_field(
                            name=f":airplane: C/S:{' '} `{callsign}`{' '} |{' '} :airplane_departure: ADEP {' '}`{departure}`{' '}  | {' '} :airplane_arriving: ADES {' '}`{arrival}`{' '} | {' '} :clock1: ETA: {' '}`{arrival_time}`",
                            value="\uFEFF",
                            inline=False
                        )
                    #In case there is error running the code it will display traceback of that error.
                    except Exception as e:
                        embed.add_field(
                            name=f"Failed to load arrivals",
                            value=f"{e}",
                            inline=False
                        )
        if not arrivals_exist:
            embed = Embed(
                title=f"Arrival Table",
                color = VATADR_RED
            )
            embed.add_field(
                name=f":x: There is no arrivals at the moment :x:",
                value="\uFEFF",
                inline=False
            )

            await interaction.followup.send(embed=embed)
        else:

            await interaction.followup.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Arrivals(bot),
        guilds= [discord.Object(id=GUILD_ID)])
        
