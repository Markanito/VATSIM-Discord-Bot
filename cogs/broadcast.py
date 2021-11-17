
import re
import random
import asyncio
from discord import Embed, Colour
import discord.utils
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import command, Cog
from discord.ext.commands.core import check, cooldown, has_any_role
import utils.json_loader


bot_config_file = utils.json_loader.read_json("config")
events_channel_id = bot_config_file["events_channel"]
news_channel_id = bot_config_file["news_channel"]
sector_file_channel_id = bot_config_file["sector_file_channel"]

class broadcast(Cog):
    def __init__(self, bot):
        self.bot = bot

#Events Broadcast
    @command(name="evbroadcast", brief="Broadcast event message in events channgel. Only usable by Staff!")
    @has_any_role("Staff", "Moderator", "Discord Admin")
    @cooldown(1, 300, BucketType.user)
    async def evbroadcast(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        with ctx.channel.typing():
            await ctx.send('What is events title?')
            title = await self.bot.wait_for('message', check=check)

            await ctx.send('What is events info? You can use formating to highlight important info.')
            desc = await self.bot.wait_for('message', check=check)

            await ctx.send('What is event website? If possible use official VATSIM URL or link to our website.')
            url = await self.bot.wait_for('message', check=check)

            await ctx.send('And now give me link to events picture.')
            picture = await self.bot.wait_for('message', check=check)

            channel = self.bot.get_channel(events_channel_id)
            evembed = Embed(title=title.content, url=url.content, description=desc.content, colour = Colour.green())
            evembed.set_image(url=picture.content)
            await channel.send(embed=evembed)
            deleted = await ctx.channel.purge(limit=9)
            await ctx.send(f"Events broadcast sent, I deleted all messages to keep the channel clean.", delete_after=10)

    #Sector File Broadcast
    @command(name="secbroadcast", brief="Broadcast message for sector file update. Only usable by Staff!")
    @has_any_role("Staff", "Moderator", "Discord Admin")
    @cooldown(1, 300, BucketType.user)
    async def secbroadcast(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        with ctx.channel.typing():
            await ctx.send('Input sector file AIRAC.')
            airac = await self.bot.wait_for('message', check=check)
        
            await ctx.send('What is new in this sector file?')
            updates = await self.bot.wait_for('message', check=check)

            channel = self.bot.get_channel(sector_file_channel_id)
            secembed = Embed(title=f'New sector file (Airac {airac.content}) is up and running', url="http://files.aero-nav.com/ADRIA", description =updates.content, color=0x0400ff)
            secembed.set_footer(text="Update guide at https://www.forum.vatadria.net/showthread.php?tid=487%22")
            await channel.send(embed=secembed)
            deleted = await ctx.channel.purge(limit=5)
            await ctx.send(f"Sector file broadcast sent, I deleted all messages to keep the channel clean. *This message will be deleted in 10 seconds!*", delete_after=10)

    #General Broadcast
    @command(name="genbroadcast", brief="Broadcast event message in events channgel. Only usable by Staff!")
    @has_any_role("Staff", "Moderator", "Discord Admin")
    @cooldown(1, 300, BucketType.user)
    async def genbroadcast(self, ctx, *, message: str):
        if len(message) == 0:
            await ctx.reply("Please provide message content for me to send!")
        channel = self.bot.get_channel(news_channel_id)
        with ctx.channel.typing():
            await channel.send(message)
            await ctx.message.delete()
            await ctx.send(f"News broadcast sent, I deleted all messages to keep the channel clean. *This message will be deleted in 10 seconds!*", delete_after=10)
    
    @command(name="push", brief="Push message for events. Only usable by Staff!")
    @has_any_role("Staff", "Moderator", "Discord Admin")
    @cooldown(1, 300, BucketType.user)
    async def push(self, ctx, *, message: str):
        if len(message) == 0:
            await ctx.reply("Please provide message content for me to send!")
        else:
            with ctx.channel.typing():
                channel = self.bot.get_channel(events_channel_id)
                await channel.send(message)
                await ctx.message.delete()
                await ctx.send(f"Push text sent, I deleted all messages to keep the channel clean. *This message will be deleted in 10 seconds!*", delete_after=10)

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(broadcast(bot))
    