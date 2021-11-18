import contextlib
import io
import os
import logging
from glob import glob
import textwrap
from traceback import format_exception
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, has_role, MissingRole, command
from discord.errors import Forbidden, HTTPException
from discord.ext.commands.errors import CommandOnCooldown
from pathlib import Path
import utils.json_loader
from utils.util import clean_code, Pag

#_____________________________________________________________________________________________________________________________________________________________________________#
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n----")
COGS = [path.split("/")[-1][:-3] for path in glob(".cogs/*.py")]


intents = discord.Intents.all()
DEFAULTPREFIX = "!"
secret_file = utils.json_loader.read_json("secrets")

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

DEFAULTPREFIX = "!"
secret_file = utils.json_loader.read_json("secrets")

bot = commands.Bot(
    command_prefix=get_prefix,
    case_insensitive=True,
    owner_id=331516683258822658,
    help_command=None,
    intents=intents
)

bot.config_token = secret_file["token"]

bot.DEFAULTPREFIX = DEFAULTPREFIX
bot.cwd = cwd
bot.blacklisted_users = []
bot.muted_users = {}
bot.version = "3.0"

#Colors for the bot, so we don't need to request it from other sources
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

@bot.event
async def on_ready():
    #When bot is ready
    print(
        f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----My current prefix is {bot.DEFAULTPREFIX}\n-----"
    )
    await bot.change_presence(
        activity=discord.Game(name="Watching !help")
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


@bot.command(name="eval", aliases=["exec"], description="Evaluates the code you provided!")
@commands.is_owner()
async def _eval(ctx, *, code):
    await ctx.reply("Let me evaluate this code for you! Won't be a sec")
    code = clean_code(code)

    local_variables = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message,
    }

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
            )

            obj = await local_variables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"
    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))

    pager = Pag(
        timeout=100,
        entries=[result[i : i + 2000] for i in range(0, len(result), 2000)],
        length=1,
        prefix="```py\n",
        suffix="```",
    )

    await pager.start(ctx)

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

bot.run(bot.config_token)
