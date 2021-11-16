from discord import Embed, Colour
import requests
import json
import math
from datetime import datetime, date, time, timezone
from discord.ext.commands.core import cooldown
from discord.ext.commands import command, Cog
from discord.ext.commands.cooldowns import BucketType

utc = datetime.now(timezone.utc)
airport = json.loads(open("airports.json").read())


class allDepartures(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="alldepartures", brief="Display departures into all VATAdria Region!")
    @cooldown(2, 60, BucketType.user)
    async def alldepartures(self, ctx,):
        t = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
        xy = json.dumps(t)
        s = json.loads(xy)
        departures_exist = False
        for item in s['pilots']:
            if item['flight_plan'] != None:
                if item['flight_plan']['departure'] in airport:
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
            await ctx.send(f"**There is no departures at the moment!**")

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(allDepartures(bot))