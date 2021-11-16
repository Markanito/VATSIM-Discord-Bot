from typing import Optional
from discord.ext import commands
from discord.ext.commands import command, Cog
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import bot_has_permissions, cooldown, has_permissions, has_role

class Clear(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="clear", aliases=["purge"], brief="Clears the messages in channel!")
    @bot_has_permissions(manage_messages=True)
    @commands.has_any_role("Staff", "Moderator", "Discord Admin")
    @cooldown(1, 500, BucketType.user)
    async def clear_messages(self, ctx, limit: Optional[int] = 10):
        with ctx.channel.typing():
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit)

            await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=5)
    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(Clear(bot))