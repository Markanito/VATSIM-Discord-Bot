from discord import Embed, Colour
import requests
import json
from discord.ext.commands import Cog, command
from datetime import datetime, timezone, date, time

guilds_ids = [692681048798265344, 572740040229388288]
url = "https://api.checkwx.com/metar/"
rule= "/decoded?pretty=1"
hdr = { 'X-API-Key': 'Insert you CheckWX API Key Here' }

class metar(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="metar", description="Get decoded METAR for <ICAO> airport", guild_ids=guilds_ids)
    async def metar(self, ctx, *, ICAO: str):

        final_url = f"{url}{ICAO}{rule}"
        req = requests.get(final_url, headers=hdr).json()
        x = json.dumps(req)
        s = json.loads(x)
        for item in s['data']:

            station_id = item['station']['name']
            raw_text = item['raw_text']
            observation = item['observed']
            observation_time = datetime.strptime(observation, '%Y-%m-%dT%H:%MZ')
            metar_time = observation_time.strftime('%H:%M')
            flight_category = item['flight_category']
            visibility = f"{item['visibility']['meters']} meters"
            temp = item['temperature']['celsius']
            dewpoint = item['dewpoint']['celsius']
            altim = item['barometer']['hpa']
            
            #Do not change values below if you don't know what they do. It is importnat to keep them as is for METAR decoding function to work properly!
            #Flight Category Color
            if flight_category == 'VFR':
                color = Colour.green()
            elif flight_category == 'MVFR':
                color = Colour.blue()
            elif flight_category == 'IFR':
                color = Colour.red()
            else:
                color = Colour.blurple()

            #Winds Builder
            try:
                wind_direction =item['wind']['degrees']
                wind_speed = item['wind']['speed_kts']
                if wind_direction == 0 and wind_speed == 0:
                    winds = 'Winds Calm'
                elif wind_direction == 0:
                    winds = f'Variable at {wind_speed}kts'
                else:
                    if wind_direction <100:
                        wind_direction = f'0{wind_direction}'
                    winds = f'{wind_direction} degrees at {wind_speed}kts'
            except:
                winds = 'Winds Calm'
                
            try:
                if item['wind']['gust_kts'] is not None:
                    wind_gust = item['wind']['gust_kts']
                    winds += f' gusting {wind_gust}kts'
            except:
                pass
 
            #Clouds Builder
            try:
                if item['clouds'][0]['code'] == 'CAVOK':
                    clouds = f'Clear Skies'
                elif item['clouds'][0]['code'] == 'CLR':
                    clouds = f'Clear Skies'
                else:
                    clouds = ''.join(f"{data['text']} at {data['feet']} feet, " for data in item['clouds'])
            except:
                clouds = f'Clear Skies'

            ##Condition Builder
            try:
                if item['conditions'] is not None:
                    condition = ''.join(f"{data['text']}, " for data in item['conditions'])
            except:
                condition = f'No conditions observed'

            #Ceiling Builder
            try:
                if item['ceiling'] is not None:
                    ceiling = ''.join(f"{item['ceiling']['text']} at {item['ceiling']['feet']},")
            except:
                ceiling = f'No ceiling observed'

            metembed = Embed(title=f"Decoded METAR for {station_id}", description=f"RAW METAR: `{raw_text}`\n\n **__METAR valid {metar_time}z\n\n__**\n_Flight Category = {flight_category}_", colour=color)
            metembed.add_field(name=":wind_chime: Winds", value=f"`{winds}`", inline=False)
            metembed.add_field(name=":eyes: Visibility", value=f"`{visibility}`", inline=False)
            metembed.add_field(name=":cloud: Clouds", value=f"`{clouds}`", inline=False)
            metembed.add_field(name=":cloud_rain: Weather", value=f"`{condition}`", inline=False)
            metembed.add_field(name="::white_sun_small_cloud: Ceiling", value=f"`{ceiling}`", inline=False)
            metembed.add_field(name=":thermometer: Temperature", value=f"`{temp}°C`", inline=False)
            metembed.add_field(name=":regional_indicator_d: Dewpoint", value=f"`{dewpoint}°C`", inline=False)
            metembed.add_field(name=":regional_indicator_q: Barometer", value=f"`{altim}`", inline=False)
            metembed.set_footer(
                text=f"Requested by {ctx.author.display_name} | For flight simulation only!",
                icon_url=ctx.author.avatar_url
            )
            await ctx.send(embed=metembed)
            
    @Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded\n-----")
def setup(bot):
    bot.add_cog(metar(bot))