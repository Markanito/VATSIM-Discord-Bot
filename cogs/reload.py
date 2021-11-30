import asyncio
from discord import Embed, Colour
import os
from datetime import datetime, timezone
from discord.colour import Color
from discord.ext.commands import command, Cog
from discord.ext.commands.core import has_role, is_owner
from glob import glob
import utils.json_loader
import traceback

#Where COGS files are saved 
COGS = [path[:-3] for path in os.listdir('./cogs') if path[-3:] == '.py']


#Roles allowed to use this commands, for now only discord admins can do this!
bot_config_file = utils.json_loader.read_json("config")
admin_role = bot_config_file["discord_admin_role_name"]
class Reload(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="reload", brief="Reload all/one of the bot cogs")
    @is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            #No cog means reload all cogs
            async with ctx.typing():
                embed = Embed(
                    title="Reloading all cogs!",
                    color = 0x808080,
                    timestamp=ctx.message.created_at

                )
                for ext in os.listdir("./cogs"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value="\uFEFF",
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=f"{e}",
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            #Reload specific cog
            async with ctx.typing():
                embed = Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)
    @command(name="cogslist", description="Get names of all cog files")
    @is_owner()
    async def cogslist(self, ctx, cog=None):
        if not cog:
            async with ctx.typing():
                embed=Embed(
                    title="Here is your requested list!",
                    color = 0x808080,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./cogs"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            embed.add_field(
                                name=f"`{ext}`",
                                value="\uFEFF",
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name="Failed to find a file!",
                                value=f"`{e}`",
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)


    @command(name="toggle", description="Enable or disable a command!")
    @is_owner()
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)

        if command is None:
            await ctx.send(f"I can't find a command with that name!")
        elif ctx.command == command:
            await ctx.send(f"You cannot disable this command.")
        else:
            command.enable = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"I have {ternary} {command.qualified_name} for you")


    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")


def setup(bot):
    bot.add_cog(Reload(bot))