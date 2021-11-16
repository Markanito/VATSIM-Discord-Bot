from discord.ext.commands import Cog, command
from discord import Embed, Colour
from discord.ext import tasks
from datetime import datetime, timezone, date, time
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import cooldown
import requests
import json
import math


airport = json.loads(open("airports.json").read())

class allArrivals(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="allarrivals",brief="Display arrivals into all VATAdria Region!")
    @cooldown(2, 60, BucketType.user)
    async def allarrivals(self, ctx,):
            t = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
            xy = json.dumps(t)
            s = json.loads(xy)
            arrivals_exist = False
            for item in s['pilots']:
                if item['flight_plan'] != None:
                    if item['flight_plan']['arrival'] in airport:
                        arrivals_exist = True
                        lan = 0.0
                        long = 0.0
                        # Positions of the airports (LAT and LONG)
                        if item['flight_plan']['arrival'] == "LDDU":
                            lan = 42.561389
                            long = 18.268333
                        elif item['flight_plan']['arrival'] == "LYBE":
                            lan = 44.819444
                            long = 20.306944
                        elif item['flight_plan']['arrival'] == "LDZA":
                            lan = 45.743056
                            long = 16.068889
                        elif item['flight_plan']['arrival'] == "LDZD":
                            lan = 44.108333
                            long = 15.346667
                        elif item['flight_plan']['arrival'] == "LDPL":
                            lan = 44.893611
                            long = 13.922222
                        elif item['flight_plan']['arrival'] == "LDSP":
                            lan = 43.538889
                            long = 16.298056
                        elif item['flight_plan']['arrival'] == "LDOS":
                            lan = 45.462778
                            long = 18.810278
                        elif item['flight_plan']['arrival'] == "LDRI":
                            lan = 45.216944
                            long = 14.570278
                        elif item['flight_plan']['arrival'] == "LJLJ":
                            lan = 46.224444
                            long = 14.456111
                        elif item['flight_plan']['arrival'] == "LJMB":
                            lan = 46.479722
                            long = 15.686111
                        elif item['flight_plan']['arrival'] == "LJPZ":
                            lan = 45.473353
                            long = 13.614978
                        elif item['flight_plan']['arrival'] == "LYPG":
                            lan = 42.359444
                            long = 19.251944
                        elif item['flight_plan']['arrival'] == "LYVR":
                            lan = 45.147778
                            long = 21.309722
                        elif item['flight_plan']['arrival'] == "LYTV":
                            lan = 42.404722
                            long = 18.723333
                        elif item['flight_plan']['arrival'] == "LYNI":
                            lan = 43.337222
                            long = 21.853611
                        elif item['flight_plan']['arrival'] == "LYKV":
                            lan = 43.818611
                            long = 20.585278
                        elif item['flight_plan']['arrival'] == "LYUZ":
                            lan = 43.898886
                            long = 19.697683
                        elif item['flight_plan']['arrival'] == "LWSK":
                            lan = 41.961111
                            long = 21.626944
                        elif item['flight_plan']['arrival'] == "LWOH":
                            lan = 41.18
                            long = 20.742222
                        elif item['flight_plan']['arrival'] == "LATI":
                            lan = 41.414722
                            long = 19.720556
                        elif item['flight_plan']['arrival'] == "LQSA":
                            lan = 43.824722
                            long = 18.331389
                        elif item['flight_plan']['arrival'] == "LQMO":
                            lan = 43.282778
                            long = 17.845833
                        elif item['flight_plan']['arrival'] == "LQBK":
                            lan = 44.936111
                            long = 17.299167
                        elif item['flight_plan']['arrival'] == "LQTZ":
                            lan = 44.458611
                            long = 18.724722
                        elif item['flight_plan']['arrival'] == "BKPR":
                            lan = 42.572778
                            long = 21.035833

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
                        depairport = item['flight_plan']['departure']
                        destairport = item['flight_plan']['arrival']
                        route = item['flight_plan']['route']

                        #Status converter
                        if int(item['flight_plan']['cruise_tas']) < 50:
                            if distance < 10:
                                status = f"Arrived at destination"
                                color = Colour.green()
                                arrival_time = f"Arrived"
                            else:
                                status = f"Preparing for the flight"
                                color = Colour.dark_orange()
                        else:
                            status = f"On the way"
                            color = Colour.blue()

                        #Time Converter, please don't fuck with this
                        if int(item['flight_plan']['cruise_tas']) > 50:
                            
                            time = distance / int(item['flight_plan']['cruise_tas'])
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
                    
                        arr1e = Embed(colour = color)
                        arr1e.set_author(name="VATAdria Arrivals")
                        arr1e.add_field(name=":id: Callsign", value=f"`{callsign}`", inline=False)
                        arr1e.add_field(name=":airplane_departure: Departure Airport", value=f"`{depairport}`", inline=False)
                        arr1e.add_field(name=":airplane_arriving: Destination Airport", value=f"`{destairport}`", inline=False)
                        arr1e.add_field(name=":airplane: Speed", value=f"`{item['flight_plan']['cruise_tas']}`", inline=False)
                        arr1e.add_field(name=":satellite_orbital: Status", value=f"`{status}`", inline=False)
                        arr1e.add_field(name=":timer:Arrival Time", value=f"`{arrival_time}`", inline=False)
                        arr1e.add_field(name=":airplane: Route", value=f"`{route}`", inline=False)
                        await ctx.send(embed=arr1e)
            if not arrivals_exist:
                await ctx.send('**There is no arrivals at the moment!**')

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(allArrivals(bot))