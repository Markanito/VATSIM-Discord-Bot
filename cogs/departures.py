from discord import Embed, Colour
from discord.ext.commands.cooldowns import BucketType
import requests
import math
import json
from datetime import datetime, date, time, timezone
from discord.ext.commands import command, Cog
from discord.ext.commands.core import cooldown

utc = datetime.now(timezone.utc)
airport = json.loads(open("airports.json").read())


class departures(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name="departures", brief="Display all departures from <ICAO> airport! <ICAO> is requried!")
    @cooldown(2, 60, BucketType.user)
    async def departures(self, ctx, *, ICAO: str):
        if len(ICAO.upper()) == 0:
            await ctx.replay("Please provide ICAO code for an airport!")

        if len(ICAO.upper()) > 4:
            await ctx.replay("ICAO provided is not valid. Check ICAO code and try agin!")

        if len(ICAO.upper()) < 4:
            await ctx.replay("ICAO provided is not valid. Check ICAO code and try agin!")

        if ICAO in airport:
            t = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
            xy = json.dumps(t)
            s = json.loads(xy)
            departures_exist = False
            for item in s['pilots']:
                if item['flight_plan'] != None:
                    if item['flight_plan']['departure'] == ICAO:
                        departures_exist = True
                        depe = Embed(colour = Colour.green())
                        depe.set_author(name="VATAdria Departures")
                        depe.add_field(name=":id: Callsign", value=item['callsign'], inline=False)
                        depe.add_field(name=":airplane_departure: Departure Airport", value=f"`{item['flight_plan']['departure']}`", inline=True)
                        depe.add_field(name=":airplane_arriving: Destination Airport", value=f"`{item['flight_plan']['arrival']}`", inline=True)
                        depe.add_field(name=":timer: Planned Dep Time", value=f"`{item['flight_plan']['deptime']}z`", inline=True)
                        depe.add_field(name=":airplane: Route", value=f"`{item['flight_plan']['route']}`", inline=True)
                        await ctx.send(embed=depe)
            if not departures_exist:
                no_depe = Embed(descrption=f":x: There is no departures from {ICAO.upper()} at the moment :x:", Colour=0xff0000)
                await ctx.send(embed=no_depe)

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(departures(bot))