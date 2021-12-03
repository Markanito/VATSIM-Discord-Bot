import asyncio
import requests
import json
import utils.json_loader
from asyncio import sleep
from discord import Embed
from discord.ext.commands import Cog, command

callsign_prefix = utils.json_loader.read_json("callsign_prefix")

positions = ["GND","TWR","APP","CTR"]

class Controller():
    def __init__(self, callsign, controller_name, frequency):
        self.callsign = callsign
        self.controller_name = controller_name
        self.frequency = frequency
    def get_callsign(self):
        return self.callsign
    def get_controller_name(self):
        return self.controller_name
    def get_frequency(self):
        return self.frequency

class online(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="online", description="Display online controllers.")
    async def online(self, ctx):
        t = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
        xy = json.dumps(t)
        s = json.loads(xy)
        online_2_cs = []
        online_2_obj = []
        online_exists = False
        for item in s['controllers']:
            callsign = item['callsign']
            frequency = item['frequency']
            controller_name = item['name']
            with ctx.typing():
                embed = Embed(
                    title=f"Online ATC Table",
                    color = 0x4c00ff,
                    timestamp = ctx.message.created_at
                )
                for i in callsign_prefix:
                    if i == callsign[:len(i)] and callsign[-3:] in positions:
                        controller_obj = Controller(callsign, controller_name, frequency)
                        online_2_obj.append(controller_obj)
                        online_2_cs.append(callsign)
                    
                for i in online_2_obj:
                    online_exists=True
                    embed.add_field(
                        name=f":id: {' '}C/S: {' '} `{i.get_callsign()}`{' '} | {' '} :man: ATCO: {' '} `{i.get_controller_name()}`{' '} | {' '} :radio: {' '} FREQ: {' '} `{i.get_frequency()}`",
                        value=f"\uFEFF",
                        inline=False
                    )
                    embed.set_footer(
                        text=f"Requested by {ctx.author.display_name}",
                        icon_url=ctx.author.avatar_url
                    )

        if online_exists:
            await ctx.send(embed=embed)
        else:
            with ctx.typing():
                embed = Embed(
                    title=f":x: No controllers online at the moment. :x:",
                    color = 0x4c00ff,
                    timestamp = ctx.message.created_at
                )
                embed.set_footer(
                    text=f"Requested by {ctx.author.display_name}",
                    icon_url=ctx.author.avatar_url
                )
                await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(online(bot))

