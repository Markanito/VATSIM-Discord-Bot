import contextlib
import io
import os
import logging
import textwrap
import json
import requests
import utils.json_loader
import discord

from discord import Intents, Embed, Colour, DMChannel
from traceback import format_exception
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, has_role, MissingRole, command
from discord.ext.commands import Bot
from discord.errors import Forbidden, HTTPException
from discord.ext.commands.errors import CommandOnCooldown
from pathlib import Path
from utils.util import clean_code, Pag

#Definig config local variables needed
cwd = Path(__file__).parents[0]
cwd = str(cwd)
COGS = [path[:-3] for path in os.listdir('./cogs') if path[-3:] == '.py']
secret_file = utils.json_loader.read_json("secrets")
config_file = utils.json_loader.read_json("config")

intents = discord.Intents.all()
DEFAULTPREFIX = config_file['default_prefix']

async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)

async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        if not data or "prefix" not in data:
            return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or(bot.DEFAULTPREFIX)(bot, message)

bot = Bot(
    command_prefix=get_prefix,
    case_insensitive=True,
    owner_id=int(config_file['owner_id']),
    help_command=None,
    intents=intents
)

#Define bot paramethers from config files
bot.DEFAULTPREFIX = DEFAULTPREFIX
bot.cwd = cwd
bot.version = "4.0"
bot.token = secret_file['token']
bot.blacklisted_users = []
bot.muted_users = {}

bot.colors = {
    "WHITE": 0xFFFFFF,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "RED": 0xE74C3C,
    "NAVY": 0x34495E,
    "DARK_AQUA": 0x11806A,
    "DARK_GREEN": 0x1F8B4C,
    "DARK_BLUE": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "DARK_ORANGE": 0xA84300,
    "DARK_RED": 0x992D22,
    "DARK_NAVY": 0x2C3E50,
}
bot.color_list = [c for c in bot.colors.values()]


#Define bot events
@bot.event
async def on_ready():
    #When bot is ready
    print(
        f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----My current prefix is {bot.DEFAULTPREFIX}\n-----"
    )
    data = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
    resp = json.dumps(data)
    s = json.loads(resp)
    users = s['general']['unique_users']
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"{users} VATSIM Users")
    )
    for cog in COGS:
        try:
            bot.unload_extension(f'cogs.{cog}')
            bot.load_extension(f'cogs.{cog}')

        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))


@bot.event
async def on_message(message):
    # Ignore messages sent by yourself
    if message.author.bot:
        return
    # A way to blacklist users from the bot by not processing commands
    # if the author is in the blacklisted_users list
    if message.author.id in bot.blacklisted_users:
        return

    # Whenever the bot is tagged, respond with its prefix
    if message.content.startswith(f"<@!{bot.user.id}>") and len(message.content) == len(
        f"<@!{bot.user.id}>"
    ):
        data = await bot.config.find_by_id(message.guild.id)
        if not data or "prefix" not in data:
            prefix = bot.DEFAULTPREFIX
        else:
            prefix = data["prefix"]
        await message.channel.send(f"My prefix here is `{prefix}`", delete_after=15)

    await bot.process_commands(message)
    
@bot.event
async def on_command_error(ctx: commands.Context, exc: Exception):
    if isinstance(exc, CommandNotFound):
        await ctx.reply("That command is not found. Use `!help` to check all available commands!")

    elif isinstance(exc, BadArgument):
        await ctx.reply("You passed bad argument, check spelling and try again")
        
    elif isinstance(exc, HTTPException):
        await ctx.reply("Unable to send a message!")

    elif isinstance(exc, MissingRole):
        await ctx.reply("You are missing required role to use this command. This means that you are not allowed to use this command")

    elif isinstance(exc, Forbidden):
        await ctx.reply("I don't have permission to do that!")

    elif isinstance(exc, CommandOnCooldown):
        await ctx.reply(f"That command is on cooldown! Try again in {exc.retry_after:,.0f} seconds.")

    elif isinstance(exc, MissingRequiredArgument):
        await ctx.reply("One or more required arguments are missing!")

    elif hasattr(exc, "original"):
        raise exc.original

    else:
        raise exc

if __name__ == "__main__":
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

bot.run(bot.token)