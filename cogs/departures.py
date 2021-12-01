import asyncio
import requests
import math
import json
import utils.json_loader
from asyncio import sleep
from datetime import datetime, date, time, timezone
from discord.ext.commands import command, Cog
from discord.ext.commands.core import cooldown
from discord import Embed, Colour
from discord.ext.commands.cooldowns import BucketType

airport = utils.json_loader.read_json("airports")

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
                    if item['flight_plan']['departure'] == (ICAO.upper()):
                        if item['groundspeed'] < 50:
                            try:
                                with ctx.typing():
                                    embed = Embed(
                                        title=f"Departure Table for {ICAO.upper()}",
                                        color = Colour.orange(),
                                        timestamp = ctx.message.created_at
                                    )
                                    departures_exist = True
                                    callsign = item['callsign']
                                    departure = item['flight_plan']['departure']
                                    arrival = item['flight_plan']['arrival']
                                    if item['flight_plan']['deptime'] == "0000":
                                        depa_time = f"Departure time unknown"
                                    else:
                                        depa_time = item['flight_plan']['deptime']
                                    
                                    embed.add_field(
                                        name=f":airplane: C/S:{' '} `{callsign}` {' '} | {' '}:airplane_departure: ADEP {' '}`{departure}`{' '} | {' '}:airplane_arriving: ADES: {' '}`{arrival}`{' '}| {' '} :clock1: ETD: {' '}`{depa_time}z`",
                                        value="\uFEFF",
                                        inline=False
                                    )
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
            if departures_exist:
                await ctx.send(embed=embed)
            else:
                embed = Embed(
                title=f"Departure Table for {ICAO.upper()}",
                color = Colour.orange(),
                timestamp = ctx.message.created_at
                )
                embed.add_field(
                    name=f":x: There is no departures at the moment :x:",
                    value="\uFEFF",
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
    bot.add_cog(departures(bot))   
