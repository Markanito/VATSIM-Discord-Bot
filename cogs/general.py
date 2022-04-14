import os
import datetime
import discord

from discord.ext import commands, tasks
from discord import app_commands
from helpers.message import staff_roles, embed
from helpers.config import COGS_LOAD, GUILD_ID, VATADR_BLUE, COGS

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="load",
        description="Load modules"
    )
    async def load(
        self,
        interaction: discord.Interaction,
        cog: str
    ) -> None:
        try:
            self.bot.load_extension(COGS_LOAD[cog])
            await interaction.response.send_message(f"`Loaded: {cog}`")
        except Exception as e:
            await interaction.response.send_message(f"**`Error:`** {type(e).__name__} - {e}")

    @app_commands.command(
        name="unload",
        description="Unload module"
    )
    async def unload(
        self,
        interaction: discord.Interaction,
        cog: str
    ) -> None:
        try:
            self.bot.unload_extension(COGS_LOAD[cog])
            await interaction.response.send_message(f"`Unloaded: {cog}`")
        except Exception as e:
            await interaction.response.send_message(f"**`Error:` {type(e).__name__} - {e}")

    @app_commands.command(
        name="cogs",
        description="Display all available modules"
    )
    async def cogs(
        self,
        interaction: discord.Interaction,
        private: bool = False
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=private)
        embed = discord.Embed(
            title=f"VATEye Cogs",
            color = VATADR_BLUE
        )
        for cog in COGS:
            embed.add_field(name=f"{cog}", value="\u2002", inline=False)
        
        await interaction.followup.send(embed=embed)

    @app_commands.command(
        name="delete",
        description="Delete specific number of messages in the channel"
    )
    async def delete(
        self,
        interaction: discord.Interaction,
        number: int = 0,
        private: bool = False
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=private)
        try:
            async for msg in interaction.channel.history(limit=number):
                msgs = await interaction.followup.send(f"Deleting messages")
                await msgs.channel.purge(limit=number)
        except Exception as e:
            await interaction.followup.send(f"`Error occured during handling command - {e}`")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Admin(bot),
        guilds= [discord.Object(id=GUILD_ID)])
        
