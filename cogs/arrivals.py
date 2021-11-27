from discord.ext.commands import Cog, command
from discord import Embed, Colour
from discord.ext.commands.cooldowns import BucketType
import requests
import math
import json
from datetime import datetime, date, time, timezone
from discord.ext.commands.core import cooldown

with open("airports.json") as json_file:
    airport = json.load(json_file)

url = "https://www.airport-data.com/api/ap_info.json?icao="

class arrivals(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="arrivals", brief="Display arrivals into <ICAO> airport! <ICAO> is required!")
    @cooldown(2, 60, BucketType.user)
    async def arrivals(self, ctx, *, ICAO: str):
        if len(ICAO) == 0:
            await ctx.replay("Please provide ICAO code for an airport!")

        if len(ICAO) > 4:
            await ctx.replay("ICAO provided is not valid. Check ICAO code and try agin!")

        if len(ICAO) < 4:
            await ctx.replay("ICAO provided is not valid. Check ICAO code and try agin!")

        if ICAO in airport:
            t = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
            xy = json.dumps(t)
            s = json.loads(xy)
            try:
                arrivals_exist = False
                for item in s['pilots']:
                    if item['flight_plan'] != None:
                        if item['flight_plan']['arrival'] == ICAO:
                            arrivals_exist = True
                            lan = 0.0
                            long = 0.0
                            airport_data_url = f"{url}{ICAO}"
                            api_data = requests.get(airport_data_url).json()
                            data = json.dumps(api_data)
                            api = json.loads(data)
                            lan = float(api['latitude'])
                            long = float(api['longitude'])

                            #distance calculation
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
                            depairport = item['flight_plan']['departure']
                            destairport = item['flight_plan']['arrival']
                            route = item['flight_plan']['route']


                            #Status converter
                            if int(item['groundspeed']) < 50:
                                if distance < 10:
                                    status = f"Arrived at destination"
                                    color = Colour.green()
                                else:
                                    status = f"Preparing for the flight"
                                    color = Colour.dark_orange()
                            else:
                                status = f"On the way"
                                color = Colour.blue()

                            #Time Converter, please don't fuck with this
                            try:
                                if int(item['groundspeed']) > 50:
                                    
                                    time = distance / int(item['groundspeed'])
                                    hour = int(time)
                                    arrival_hour = utc.hour + hour
                                    arrival_minute = utc.minute + int((time - int(time))*60)
                                    if arrival_minute <10:
                                        arrival_time = f"{arrival_hour}:0{arrival_minute}z"

                                    elif 10 < arrival_minute < 59:
                                        arrival_time = f"{arrival_hour}:{arrival_minute}z"

                                    elif arrival_minute > 59:
                                        add_hour = int(arrival_minute / 60)
                                        arrival_minute = int(((arrival_minute / 60) - add_hour) * 60)
                                        arrival_hour = arrival_hour + add_hour
                                            
                                        if arrival_hour > 23:
                                            days = int(arrival_hour / 24)
                                            arrival_hour = (arrival_hour - (days * 24))
                                            if days == 1:
                                                if arrival_minute < 10:
                                                    arrival_time = f"{arrival_hour}:0{arrival_minute}z tomorrow"
                                                else:
                                                    arrival_time = f"{arrival_hour}:{arrival_minute}z tomorrow"
                                    else:
                                        arrival_time= f"{arrival_hour}:{arrival_minute}z"
                                else:
                                    arrival_time = f"Plane is on the ground."
                            except:
                                arrival_time = f"Plane is on the ground"

                            
                            #Status converter
                            if int(item['groundspeed']) < 70:
                                if distance < 10:
                                    status = f"Arrived at destination"
                                    color = Colour.green()
                                else:
                                    status = f"Preparing for the flight"
                                    color = Colour.dark_orange()
                            else:
                                status = f"On the way"
                                color = Colour.blue()
                            
                            arr1e = Embed(colour = color)
                            arr1e.set_author(name="VATAdria Arrivals")
                            arr1e.add_field(name=":id: Callsign", value=f"`{callsign}`", inline=False)
                            arr1e.add_field(name=":airplane_departure: Departure Airport", value=f"`{depairport}`", inline=False)
                            arr1e.add_field(name=":airplane_arriving: Destination Airport", value=f"`{destairport}`", inline=False)
                            arr1e.add_field(name=":satellite_orbital: Status", value=f"`{status}`", inline=False)
                            arr1e.add_field(name=":timer:Arrival Time", value=f"`{arrival_time}`", inline=False)
                            arr1e.add_field(name=":airplane: Route", value=f"`{route}`", inline=False)
                            await ctx.send(embed=arr1e)

                if not arrivals_exist:
                    await ctx.send(f"**There is no arrivals to {ICAO} at the moment!**")

            except Exception as e:
                await ctx.send('There was exception running this command!\n`{}: {}`'.format(type(e).__name__, e))

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(arrivals(bot))