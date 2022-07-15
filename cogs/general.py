from contextvars import Context
import os
import datetime
from typing import Optional, Literal
import discord

from discord.ext import commands, tasks
from discord import Object, app_commands
from helpers.message import staff_roles, embed
from helpers.config import COGS_LOAD, GUILD_ID, STAFF_ROLES, VATADR_BLUE, COGS

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: Context, guilds: commands.Greedy[Object], spec: Optional[Literal["~"]] = None) -> None:
        """Command to sync all commands to a guild. This is required since there is bug with discord where Slash commands are not registered."""
        if not guilds:
            if spec == "~":
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.treee.copy_global_to(guild=ctx.guild)
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            else:
                fmt = await ctx.bot.tree.sync()

            await ctx.send(f"Synced {len(fmt)} commands {'globally' if spec is None else 'to the current guild.'}")

            fmt = 0
            for guild in guilds:
                try:
                    await ctx.bot.tree.sync(guild=guild)
                except discord.HTTPException:
                    pass
                else:
                    fmt += 1
                
            await ctx.send(f"Synced the tree to {fmt}/{len(guilds)} guilds")

    @app_commands.command(
        name="load",
        description="Load modules"
    )
    @app_commands.checks.has_any_role(*staff_roles())
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
    @app_commands.checks.has_any_role(*staff_roles())
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
    @app_commands.checks.has_any_role(*staff_roles())
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
    @app_commands.checks.has_any_role(*staff_roles())
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
        
