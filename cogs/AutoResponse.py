import discord
import asyncio
import json

from discord.ext import commands
from helpers.config import BOT_CHANNEL, GUILD_ID, BOT_CHANNEL

class AutoResponder(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        with open("./data/AutoResponder.json") as f:
            self.responses = json.load(f)

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message):
        if message.guild != None:
            return
        
        await asyncio.sleep(3) # ReteLimit Countermeasure

        await self.DMLog(message)
        
        if message.author.bot:
            return

        for response in self.responses:
            if response in message.content.lower():
                return await message.author.send(self.responses[response])


    async def DMLog(self, message):
        try:
            dmschan = await self.bot.fetch_channel(BOT_CHANNEL)
            if message.content and message.content != '':
                if message.author != self.bot.user:
                    await dmschan.send(embed=self.Embed("User Message", message.content))
                else:
                    await dmschan.send(embed=self.Embed("VATEye Response", message.content))
        except:
            return

    def Embed(self, author, description):
        embed = discord.Embed(
                description = description,
                colour = 0xc70300
                )
        embed.set_author(name=author)

        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        AutoResponder(bot),
        guilds= [discord.Object(id=GUILD_ID)])
        