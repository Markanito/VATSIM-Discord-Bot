import os
import re
import discord
import requests
import datetime


from discord import app_commands
from dotenv import load_dotenv
from discord.ext import commands, tasks
from helpers.message import staff_roles
from helpers.config import MENTOR_ROLE, VATSIM_MEMBER_ROLE, VATSIM_SUBDIVISION, CHECK_MEMBERS_INTERVAL, VATADR_MEMBER_ROLE, ROLE_REASONS, GUILD_ID, VATADR_ATC_ROLE, VATADR_STAFF_ROLE, VATADR_TRAINING_ROLE, VATADR_VISITING_ROLE, VATSIM_API_TOKEN, VATSIM_CHECK_MEMBER_URL

load_dotenv('.env')



class TasksCog(commands.Cog):
    vatadr_ROLE_ADD_REASON = ROLE_REASONS['vatadr_add']
    vatadr_ROLE_REMOVE_REASON = ROLE_REASONS['vatadr_remove']
    NO_CID_REMOVE_REASON = ROLE_REASONS['no_cid']
    NO_AUTH_REMOVE_REASON = ROLE_REASONS['no_auth']

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.check_members_loop.start()

    def cog_unload(self):
        self.check_members_loop.cancel()


    async def check_members(self, override=False):
        """
        Task checks guild members and assigns roles according to the data we've stored in our system
        :return:
        """

        await self.bot.wait_until_ready()

        print("check_members started at " + str(datetime.datetime.now().isoformat()))

        guild = self.bot.get_guild(GUILD_ID)
        users = guild.members

        vatadr_member = discord.utils.get(guild.roles, id=VATADR_MEMBER_ROLE)
        vatsim_member = discord.utils.get(guild.roles, id=VATSIM_MEMBER_ROLE)

        request = requests.get(VATSIM_CHECK_MEMBER_URL, headers={'Authorization': 'Token ' + VATSIM_API_TOKEN})
        if request.status_code == requests.codes.ok:
            data = request.json()
            
        for user in users:            
            try:
                cid = re.findall('\d+', str(user.nick))

                should_have_vatadr = False
                if len(cid) < 1:
                    raise ValueError
                for item in data['results']:
                    if int(item['id']) == int(cid[0]) and str(item['subdivision']) == str(VATSIM_SUBDIVISION):
                        should_have_vatadr = True
                
                if vatsim_member in user.roles:
                    if vatadr_member not in user.roles and should_have_vatadr == True:
                        await user.add_roles(vatadr_member, reason=self.vatadr_ROLE_ADD_REASON)
                    elif vatadr_member in user.roles and should_have_vatadr == False:
                        await user.remove_roles(vatadr_member, reason=self.vatadr_ROLE_REMOVE_REASON)
                elif vatsim_member not in user.roles and vatadr_member in user.roles:
                    await user.remove_roles(vatadr_member, reason=self.NO_AUTH_REMOVE_REASON)
                
                print(f"Assigned Local Member role to: {cid[0]}")

            except ValueError as e:
                if vatadr_member in user.roles:
                    await user.remove_roles(vatadr_member, reason=self.NO_CID_REMOVE_REASON)
            except Exception as e:
                print(e)
                continue

            

                
        print("check_members finished at " + str(datetime.datetime.now().isoformat()))


    @tasks.loop(seconds=CHECK_MEMBERS_INTERVAL)
    async def check_members_loop(self):
        await self.check_members()

    
    @app_commands.command(
        name="checkusers",
        description="Refresh roles based on division membership"
    )
    async def user_check(
        self,
        interaction: discord.Interaction,
        private: bool = False
    ):
        await interaction.response.defer(thinking=True, ephemeral=private)
        await self.check_members(True)
        await interaction.followup.send("Member refresh process finished")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        TasksCog(bot),
        guilds= [discord.Object(id=GUILD_ID)])