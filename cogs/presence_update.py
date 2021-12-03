import requests
import json
import discord
from discord.ext.commands import Cog
from discord.ext import tasks

#This will update bot presence every 5 minutes with how many unique VATSIM users are online. This can be disabled by adding _ in front of the filename

class Update(Cog):
    def __init__(self, bot):
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

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(Update(bot))