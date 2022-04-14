import discord
import emoji

from helpers.config import GUILD_ID, REACTION_ROLES, REACTION_MESSAGE_IDS, REACTION_EMOJI, ROLE_REASONS, ROLES_CHANNEL
from discord.ext import commands

class RoleReact(commands.Cog):
    def __init__(self, bot: commands.Bot) ->None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(ROLES_CHANNEL)
        msg = await channel.fetch_message(channel.last_message_id)
        guild = self.bot.get_guild(GUILD_ID)
        emojies = emoji.demojize(payload.emoji.name)
        for message in REACTION_MESSAGE_IDS:
            if int(msg.id) == int(message) and emojies in REACTION_EMOJI:
                role = discord.utils.get(guild.roles, id=int(REACTION_ROLES[emojies]))
                user = guild.get_member(payload.user_id)
                if role not in user.roles:
                    await user.add_roles(role, reason=ROLE_REASONS['reaction_add'])
                    await user.send(f"You have been given the `{role.name}` because you reacted with {payload.emoji}!")


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(GUILD_ID)
        emojies = emoji.demojize(payload.emoji.name)
        for message in REACTION_MESSAGE_IDS:
            if int(msg.id) == int(message) and emojies in REACTION_EMOJI:
                role = discord.utils.get(guild.roles, id=int(REACTION_ROLES[emojies]))
                user = guild.get_member(payload.user_id)
                if role in user.roles:
                    await user.remove_roles(role, reason=ROLE_REASONS['reaction_remove'])
                    await user.send(f'You no longer have the `{role.name}` role because you removed your reaction.')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        RoleReact(bot),
        guilds= [discord.Object(id=GUILD_ID)])
