import discord
import os
import requests
import re
import emoji
import json
import aiohttp

from discord.ext import commands
from dotenv import load_dotenv
from helpers.config import VATADR_MEMBER_ROLE, VATSIM_MEMBER_ROLE, VATSIM_SUBDIVISION, GUILD_ID, BOT_TOKEN, REACTION_ROLES, REACTION_MESSAGE_IDS, REACTION_EMOJI, ROLE_REASONS
from helpers.members import get_division_members
from helpers import config

load_dotenv('env')


class VATEye(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            application_id = 743941860178788452
        )

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        await config.load_cogs(self)
        await bot.tree.sync(guild = discord.Object(id = GUILD_ID))


    async def on_ready(self) -> None:
        print(f"Bot started. \nUsername: {self.user.name}. \nID: {self.user.id}\nDiscord Version: {discord.__version__}")

        try:
            await self.change_presence(activity=config.activity(), status=config.status())
        except Exception as e:
            print(f"Error changing presence. Exception: {e}")

    async def on_member_update(self, before_update, user: discord.User):
        if (before_update.nick == user.nick):
            return
        
        guild = self.get_guild(GUILD_ID)

        vatadr_member = discord.utils.get(guild.roles, id=VATADR_MEMBER_ROLE)
        vatsim_member = discord.utils.get(guild.roles, id=VATSIM_MEMBER_ROLE)

        try:
            cid = re.findall('\d+', str(user.nick))

            if len(cid) < 1:
                raise ValueError

            api_data = await get_division_members()

            should_have_vatadr = False

            for entry in api_data:
                if int(entry['id']) == int(cid[0]) and str(entry["subdivision"]) == str(VATSIM_SUBDIVISION):
                    should_have_vatadr = True

            if vatsim_member in user.roles:
                if vatadr_member not in user.roles and should_have_vatadr == True:
                    await user.add_roles(vatadr_member)
                elif vatadr_member in user.roles and should_have_vatadr == False:
                    await user.remove_roles(vatadr_member)
            elif vatsim_member not in user.roles and vatadr_member in user.roles:
                await user.remove_roles(vatadr_member)
        except ValueError as e:
            print(f"Tried to find an ID but it ther a ValueError, not found!")

        except Exception as e:
            print(f"{e}")


bot = VATEye()
try:
    bot.run(BOT_TOKEN)
except Exception as e:
    print(f"Error occured while starting the bot: {e}")