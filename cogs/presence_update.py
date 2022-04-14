from hikari import PresenceUpdateEvent
import requests
import json
import discord

from discord.ext import tasks, commands
from helpers.config import GUILD_ID

#This will update bot presence every 5 minutes with how many unique VATSIM users are online. This can be disabled by adding _ in front of the filename

class Update(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.update_presence.start()

    def cog_unload(self):
        self.update_presence.cancel()

    @tasks.loop(minutes=5)
    async def update_presence(self):
        try:
            data = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
            resp = json.dumps(data)
            s = json.loads(resp)
            users = s['general']['unique_users']
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=f"{users} VATSIM Users")
            )
        except:
            print(f"Bot instance not found, skipping presence update for now!")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Update(bot),
        guilds= [discord.Object(id=GUILD_ID)])
