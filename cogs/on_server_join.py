from discord import Embed, Colour
from discord import colour
from discord.ext.commands import Cog, command

class ServerJoin(Cog):

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_guild_join(self, guild):
        #Send message to unverified channel!
        channel = self.bot.get_channel(805011846326648862)
        await channel.send(
            ":flag_al: :flag_hr: :flag_rs: :flag_si: :flag_ba: :flag_me: :flag_mk: :flag_xk:  **Welcome to the VATSIM Adria Discord!** :flag_al::flag_hr: :flag_rs: :flag_si: :flag_ba: :flag_me: :flag_mk: :flag_xk: \n\n:see_no_evil:**I want to chat, how can I do this?**Go to https://community.vatsim.net/ and link your Discord account and VATSIM Accounts. You will then be given the Verified Member role and be able to view the server in its full glory. \n\n:question: **I am a staff member or local controller and can view channels but can not type. What is wrong?**Your roles have the permissions to view the channels. To be able to type in them, go to https://community.vatsim.net/ and after linking your Discord and VATSIM accounts, head over to the `Joined section`, look for this server, click on `Edit Username`, select your preferred choice, and accept. Then we can start chatting again!:cry: \n**It's still not working, what do I do?** If you have troubles, let us know and we'll try to help you out!"
        )


        #Send message when bot is deployed on the server. This is just to make sure everyone know we replaced old bot with better and new one!
        channel = self.bot.get_channel(686512894065770586)
        await channel.send("Hello @everyone. \n\nI just joined this server, my name might sound familiar to you but I am new and refreshed bot to server VATAdria server. My older brother is now retired and I will take his place. \n\nTo start using me type in `!help` to see all available commands!")


        #Rules channel
        channel = self.bot.get_channel(722128191954878505)
        rules_embed = Embed(title="Rules",colour=0x00ff40)
        rules_embed.add_field(name='**Discord Terms of Service & Community Guidelines**', value="We ask that all members of our Discord Community abide by Discord's Community Guidelines and Terms of Service at all times.\n ToS — https://discord.com/terms\n Guidelines — https://discord.com/guidelines", inline=False)
        rules_embed.add_field(name='**VATSIM Code of Conduct**', value="We ask that all members of our Discord Community abide by VATSIM's Code of Conduct at all times. \nVATSIM CoC — https://www.vatsim.net/documents/code-of-conduct", inline=False)
        rules_embed.add_field(name='**Spam, Sharing Malicious Links, and sending links in the wrong channels is not allowed**', value="Sending messages rapidly, sending the same message over and over again, posting links with inappropriate content, and redirects to viruses, phishing sites or similar is not allowed.", inline=False)
        rules_embed.add_field(name='**Arguing vs. Debates**', value="Debates are allowed as long as they stay constructive and respectful. Civilized conversation will always be welcome, but we ask that all parties involved maintain a level head and respect other individuals who have differing opinions.", inline=False)
        await channel.send(embed=rules_embed)

        rules_embed2 = Embed(Title="Rules", colour=0x00ff40)
        rules_embed2.add_field(name='**Harassment & Inappropriate Chat**', value="Name calling, bullying, swearing at, and belittling other people is not allowed under any circumstance. Harassing VATSIM Staff & Developers regarding upcoming new features, suspensions, applications, etc. is not allowed under any circumstance. Please only reach out through the proper channels if you have any questions or concerns for the VATSIM Staff Team.", inline=False)
        rules_embed2.add_field(name='**Voice Chat - Be Mindful**', value="When utilizing a voice chat channel, please be mindful of other individuals in the channel with you. This means no yelling or screaming, making obscene noises, and leaving your microphone open for long periods of time with only ambient audio or music playing in the background.", inline=False)
        rules_embed2.add_field(name='**Voice Chat Usage**', value="Please do not use public voice channels to conduct private matters. If a user joins your voice channel, please do not ask them to leave due to the conversation you are having, please switch to a private call or another discord server to have private discussions.", inline=False)
        rules_embed2.add_field(name='**Roles & Mentions**', value="Please do not excessively mention specific roles or individuals, including VATSIM Adria Staff Members.", inline=False)
        rules_embed2.add_field(name='**Enforcement**', value="All Discord Rules are enforced by members of the VATSIM Adria Staff Team. Depending on the severity of an infraction, cases can be escalated to a VATSIM Network Supervisor for further review.", inline=False)
        await channel.send(embed=rules_embed2)

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")      
def setup(bot):
    bot.add_cog(ServerJoin(bot))