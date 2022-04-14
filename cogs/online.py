import discord
import requests
import json
import utils.json_loader

from discord import app_commands, Embed, Colour
from discord.ext import commands
from helpers.config import GUILD_ID, VATADR_RED, VATADR_BLUE

callsign_prefix = utils.json_loader.read_json("callsign_prefix")
positions = ["GND", "TWR", "APP", "CTR"]

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

class Online(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(
        name="online",
        description="Display all online controllers"
    )
    async def online(
        self,
        interaction: discord.Interaction,
        private: bool = False
    ):
        await interaction.response.defer(thinking=True, ephemeral=private)
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
            embed = Embed(
                title=f"Online ATC Table",
                color = VATADR_BLUE,
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

        if online_exists:
            await interaction.followup.send(embed=embed)
        else:
            embed = Embed(
                title=f":x: No controllers online at the moment. :x:",
                color = VATADR_RED
            )
            await interaction.followup.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Online(bot),
        guilds= [discord.Object(id=GUILD_ID)])
        
