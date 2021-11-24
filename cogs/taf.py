import pytaf
from discord import Embed, Colour
import requests
import json
from discord.ext.commands import Cog, command
from datetime import datetime, timezone, date, time
import utils.json_loader


bot_config_file = utils.json_loader.read_json("config")
checkwxapikey = bot_config_file["checkwx_api_key"]
url = "https://api.checkwx.com/taf/"
rule= "/decoded?pretty=1"
hdr = { 'X-API-Key': checkwxapikey }
class taf(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="taf", description="Get decoded taf for airport")
    async def taf(self, ctx, *, ICAO: str):
        final_url = f"{url}{ICAO}{rule}"
        req = requests.get(final_url, headers=hdr).json()
        x = json.dumps(req)
        s = json.loads(x)
        for item in s['data']:
            station_id = item['station']['name']
            raw_taf = item['raw_text']
            taf = pytaf.TAF(raw_taf)
            decoder = pytaf.Decoder(taf)

            taf_embed = Embed(title=f"Decoded TAF for {item['icao']} aerodrome", description=f"\nRAW TAF: `{item['raw_text']}`\n\n\n __Decoded TAF__\n\n**{decoder.decode_taf()}**\n\n", colour=0x4c00ff)
            taf_embed.set_footer(
                text=f"Requested by {ctx.author.display_name} | For flight simulation only!",
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=taf_embed)




    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(taf(bot))