import discord
from datetime import datetime, timezone
from discord.colour import Color
from discord.ext.commands import command, Cog
from discord.ext.commands.core import has_role
from glob import glob
import utils.json_loader

#Where COGS files are saved 
COGS = [path.split("/")[-1][:-3] for path in glob("./cogs/*.py")]


#Roles allowed to use this commands, for now only discord admins can do this!
bot_config_file = utils.json_loader.read_json("config")
admin_role = bot_config_file["discord_admin_role_name"]
class Reload(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="load", brief="Load a new command")
    @has_role(str(admin_role))
    async def load(self, ctx, *, cog: str):
        try:
            for cogs in COGS:
                self.bot.load_extension(f'cogs.{cog}')
                loadEmbed = discord.Embed(title=f":thumbsup: Loaded {cog} successfully! :thumbsup:", color = discord.Colour.green())
                await ctx.send(embed=loadEmbed, delete_after=5)
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))

    @command(name="unload", brief="Unload a command")
    @has_role(str(admin_role))
    async def unload(self, ctx, *, cog: str):
        try:
            for cogs in COGS:
                self.bot.unload_extension(f'cogs.{cog}')
                
                unloadEmbed = discord.Embed(title=f":thumbsup: Unloaded {cog} successfully! :thumbsup:", color = discord.Colour.red())
                await ctx.send(embed=unloadEmbed, delete_after=5)
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))

    @command(name="reload", brief="Reload all commands")
    @has_role(str(admin_role))
    async def reload(self, ctx):
        for cog in COGS:
            try:
                self.bot.unload_extension(f'cogs.{cog}')
                self.bot.load_extension(f'cogs.{cog}')
                reloadEmbed = discord.Embed(title=f":thumbsup: Reloaded {cog} successfully! :thumbsup:", color = discord.Colour.green())
                await ctx.send(embed=reloadEmbed)
            except Exception as e:
                await ctx.send('{}: {}'.format(type(e).__name__, e))
                
    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(Reload(bot))