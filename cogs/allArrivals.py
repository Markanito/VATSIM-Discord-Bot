import asyncio
import math
import requests
import json
import utils.json_loader
from asyncio import sleep
from discord import Embed, Colour
from discord.ext.commands import Cog, command
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import cooldown
from datetime import datetime, timezone, date, time

airport = utils.json_loader.read_json("airports")

url = "https://www.airport-data.com/api/ap_info.json?icao="

class Arrivals(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="allarrivals", description="Display all arrivals to Adria region!")
    @cooldown(2, 60, BucketType.user)
    async def allarrivalstest(self, ctx):
        resp = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
        data = json.dumps(resp)
        s = json.loads(data)
        arrivals_exist = False
        for item in s['pilots']:
            if item['flight_plan'] != None:
                if item['flight_plan']['arrival'] in airport:
                    try:
                        with ctx.typing():
                            embed = Embed(
                                title="Arrival Table",
                                color = Colour.blue(),
                                timestamp = ctx.message.created_at
                            )
                            arrivals_exist = True
                            #This is just a way to convert ICAO of BKPR to LYPR due to API differences in ICAO codes
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
                    await asyncio.sleep(0.5)
                    embed.set_footer(
                        text=f"Requested by {ctx.author.display_name}",
                        icon_url=ctx.author.avatar_url
                    )
        if arrivals_exist:
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title=f"Arrivals Table",
                color = Colour.blue(),
                timestamp = ctx.message.created_at
            )
            embed.add_field(
                name=f":x: No arrivals at the moment. :x:",
                value=f"\uFEFF",
                inline=False
            )
            embed.set_footer(
                text=f"Requested by {ctx.author.display_name}",
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=embed)
            

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")

def setup(bot):
    bot.add_cog(Arrivals(bot))   
