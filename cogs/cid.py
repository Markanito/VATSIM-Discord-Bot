from discord import Embed
from discord.ext.commands import Cog, command
from discord.ext.commands.core import has_any_role
import requests
import json
import utils.json_loader

bot_config_file = utils.json_loader.read_json("config")
events_channel_id = bot_config_file["events_channel"]
news_channel_id = bot_config_file["news_channel"]
sector_file_channel_id = bot_config_file["sector_file_channel"]
staff_role = bot_config_file['staff_role_name']
admin_role = bot_config_file['discord_admin_role_name']
moderator_role = bot_config_file['moderator_role_name']

class cid(Cog):
    def __init__(self, bot):
        self.bot = bot


    @command(name="cid", description="Get user info by ID, only usable by Staff members.")
    @has_any_role(str(staff_role), str(admin_role), str(moderator_role))
    async def cid(self, ctx, *, cid: int):
        vatsim_id = int(cid)
        data_url = "https://api.vatsim.net/api/ratings/"
        rule = "?format=json"
        rule_2 = "/rating_times/?format=json"
        data_url_final = f"{data_url}{vatsim_id}{rule}"
        hours_url_final = f"{data_url}{vatsim_id}{rule_2}"
        data = requests.get(data_url_final).json()
        hours = requests.get(hours_url_final).json()

        #Rating & Color converter
        if data['rating'] == -1:
            rating = "Inactive - `INAC`"
            color = 0xff0000
        elif data['rating'] == -0:
            rating = "Suspended - `SUS`"
            color = 0xff0000
        elif data['rating'] == 1:
            rating = "Observer - `OBS`"
            color = 0x11ff00
        elif data['rating'] == 2:
            rating = "Tower Trainee - `S1`"
            color = 0x11ff00
        elif data['rating'] == 3:
            rating = "Tower Controller - `S2`"
            color = 0x11ff00
        elif data['rating'] == 4:
            rating = "Senior Student - `S3`"
            color = 0x11ff00
        elif data['rating'] == 5:
            rating = "Enroute Controller - `C1`"
            color = 0x0040ff
        elif data['rating'] == 6:
            rating = "Controller 2 - `C2`"
            color = 0x0040ff
        elif data['rating'] == 7:
            rating = "Senior Controller - `C3`"
            color = 0x0040ff
        elif data['rating'] == 8:
            rating = "Instructor - `I1`"
            color = 0xc8ff00
        elif data['rating'] == 9:
            rating = "Instructor 2 - `I2`"
            color = 0xc8ff00
        elif data['rating'] == 10:
            rating = "Senior Instructor - `I3`"
            color = 0xc8ff00
        elif data['rating'] == 11:
            rating = "Supervisor - `SUP`"
            color = 0x8000ff
        elif data['rating'] == 12:
            rating = "Administrator - `ADM`"
            color = 0x8000ff
        else:
            rating = "Unknown"
            color = 0xff00bb

        #Pilot rating Builder
        if data['pilotrating'] == 0:
            pilot_rating = "Basic Member - `NEW`"
        elif data['pilotrating'] == 1:
            pilot_rating = "Private Pilot Licence - `PPL`"
        elif data['pilotrating'] == 3:
            pilot_rating = "Instrument Rating - `IR`"
        elif data['pilotrating'] == 7:
            pilot_rating = "Commercial Multi-Engine License - `CMEL`"
        elif data['pilotrating'] == 15:
            pilot_rating = "Airline Transport Pilot License - `ATPL`"
        else:
            pilot_rating = "Unknown"


        stats_embed = Embed(title=f"Statistics for VATSIM user`{cid}`", color=color)
        stats_embed.add_field(name="Controller rating", value=f"__{rating}__", inline=True)
        stats_embed.add_field(name="Pilot rating", value=f"__{pilot_rating}__", inline=True)
        stats_embed.add_field(name="Subdivision", value=f"**{data['subdivision']}**", inline=True)
        stats_embed.add_field(name="ATC hours", value=f"**{hours['atc']}**", inline=True)
        stats_embed.add_field(name="Pilot hours", value=f"**{hours['pilot']}**", inline=True)
        stats_embed.add_field(name="S1 hours", value=f"**{hours['s1']}**", inline=True)
        stats_embed.add_field(name="S2 hours", value=f"**{hours['s2']}**", inline=True)
        stats_embed.add_field(name="S3 hours", value=f"**{hours['s3']}**", inline=True)
        stats_embed.add_field(name="C1 hours", value=f"**{hours['c1']}**", inline=True)
        stats_embed.add_field(name="C3 hours", value=f"**{hours['c3']}**", inline=True)
        stats_embed.add_field(name="I1 hours", value=f"**{hours['i1']}**", inline=True)
        stats_embed.add_field(name="I3 hours", value=f"**{hours['i3']}**", inline=True)
        stats_embed.set_footer(
            text=f"Requested by {ctx.author.display_name} | Staff info only.",
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=stats_embed)





    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(cid(bot))