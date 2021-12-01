import asyncio
import requests
import json
import utils.json_loader
from asyncio import sleep
from discord import Embed, Colour
from discord.ext.commands import Cog, command, cooldown, BucketType

airport = utils.json_loader.read_json("airports")

class Departures(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="alldepartures", description="Display all departures")
    @cooldown(2, 60, BucketType.user)
    async def alldepartures(self, ctx):
        data = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
        resp = json.dumps(data)
        s = json.loads(resp)    
        deparutres_exist = False
        for item in s['pilots']:
            if item['flight_plan'] != None:
                if item['flight_plan']['departure'] in airport and item['groundspeed'] < 50:
                    try:
                        with ctx.typing():
                            embed = Embed(
                                title="Departure Table",
                                color = Colour.orange(),
                                timestamp = ctx.message.created_at
                            )
                            deparutres_exist=True
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
        if deparutres_exist:
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title=f"Departure Table",
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
    bot.add_cog(Departures(bot))   
