import os
import discord
import emoji
import re

from discord import Embed
from helpers.config import GUILD_ID, REACTION_ROLES, REACTION_EMOJI, ROLE_REASONS, RULES_CHANNEL, ROLES_CHANNEL, VATADR_BLUE
from discord.ext import commands

class ServerJoin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        welcome_channel = self.bot.get_channel(RULES_CHANNEL)
        roles_channel = self.bot.get_channel(ROLES_CHANNEL)

        await welcome_channel.purge(limit=5)
        print(f"Purged welcome_channel")
        await roles_channel.purge(limit=5)
        print(f"Purged roles_channel")

        description =f"**Welcome to the Discord server of VATSIM Adria!**\n\nTo gain access to this server, please follow the instructions sent by the Vatsim Bot or log in here: https://community.vatsim.net/\n\n:bell: If you want to be added to the notification list, visit the #role-react channel after verifying your account\n\n▫️▫️▫️\n\n:bookmark: VATSIM Adria provide a Discord server for its members. This server may however be freely used by any member of VATSIM Adria or its parent organizations, who adheres to the following rules:\n\n:one: We ask that all members of our Discord Community abide by Discord's Community Guidelines and Terms of Service at all times!\n:two: We ask that all members of our Discord Community Abide by VATSIM's Code of Conduct at all times!\n\n:three: Sending messages rapidly, sending the same message over and over again, posting links with inapopriate content, and redirects to viruses, phishing sites or similar is not allowed!\n\n:four: Treat each other with mutual respect. Don't threat, harass or belittle other members\n\n:five: Sharing of illegal information, such as information about pirated software, is strictly prohibited\n\n:six: Avoid unneccessary noises in voice channels, that might be to annoyance for others\n\n:seven: Adhere to instrcutions from the staff. Staff members is spotted by their visible rank\n:eight: Do not enter any of the training department rooms unless you have a scheduled training or checkout. Use the 'Waiting room' if you have a planned session. Adjacent controllers may enter for coordination\n\n:nine: Debates are allowed as long as they stay constructive and respectful. Civilized conversation will always be welcom, but we ask that all parties involved maintain a level head and respect other individuals who have different opinion. Name calling, bullying, swearing at, adn belittling other people is not allowed under any circumstance. Harrasing VATSIM & VATSIM Adria Staff & Developers regarding upcoming features, suspenisons, applications, etc is not allowed under any circumstance. Please only reach out through the propper channels if you have any questions of concers for the VATSIM Adria Staff Team.\n\n▫️▫️▫\n\n\n_By verifying your account on this Discord server, you agree to [Vatsim Adria's Data Protection Policy](https://vatadria.com/files/Data_Protection_Policy.pdf)._"
        welcome_embed = Embed(
            title=f"Rules",
            description=f"{description}",
            color= VATADR_BLUE
        )

        await welcome_channel.send(embed=welcome_embed)

        roles_embed = Embed(
            title=f"React to claim a role!",
            description=f":star: Do you want to get notified about VATSIM Adria Events? In that case <@&951114644288831518> is perfect for you! We will ping you once our event is posted and send reminder 2 hours before event so you don't forget about it ;).\\n\nYou are pilot on the network and want to get access to pilot specific channels? Then <@&781843274922590228> is perfect for you!",
            color=VATADR_BLUE
        )
        await roles_channel.send(f"In order to ensure we don't spam our lovely members with a ton of pings, we've created tags for our bot to ping depending on the content we're posting about. Simply react below with the corresponding emojis to have the roles assigned. If you no longer want to get notified simply remove reaction from the message and you will no longer be pinged.")
        embed_message = await roles_channel.send(embed=roles_embed)
        await embed_message.add_reaction("⭐")
        await embed_message.add_reaction("👨‍✈️")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        ServerJoin(bot),
        guilds= [discord.Object(id=GUILD_ID)])
