import discord
import pytaf
import requests
import json

from discord import app_commands
from discord import Embed, Colour
from discord.ext import commands
from datetime import datetime, timezone, date, time
from typing import final
from helpers.config import GUILD_ID, VATADR_BLUE, CHECKWX_API_KEY

rule= "/decoded?pretty=1"
hdr = { 'X-API-Key': CHECKWX_API_KEY }


class Metar(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="metar",
        description="Fetch decoded METAR for airport!")

    async def metar(
        self,
        interaction: discord.Interaction,
        airport: str,
        private: bool = False
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=private)
        url="https://api.checkwx.com/metar/"
        final_url=f"{url}{airport.upper()}{rule}"
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
            temp_f = item['temperature']['fahrenheit']
            dewpoint = item['dewpoint']['celsius']
            dewpoint_f = item['dewpoint']['fahrenheit']
            altimq = item['barometer']['hpa']
            altima = item['barometer']['hg']
            humidity = item['humidity']['percent']
                
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
                    clouds = ''.join(f"{data['text']} at {data['feet']} feet\n" for data in item['clouds'])
            except:
                clouds = f'Clear Skies'

            #Condition Builder
            try:
                if item['conditions'] is not None:
                    condition = ''.join(f"{data['text']}\n" for data in item['conditions'])
            except:
                condition = f'No conditions observed'

            #Ceiling Builder
            try:
                if item['ceiling'] is not None:
                    ceiling = ''.join(f"{item['ceiling']['text']} at {item['ceiling']['feet']}\n")
            except:
                ceiling = f'No ceiling observed'

            metembed = Embed(title=f"Decoded METAR for {station_id}", description=f"RAW METAR: `{raw_text}`\n\n **__METAR valid {metar_time}z\n\n__**\n_Flight Category = {flight_category}_", colour=color)
            metembed.add_field(name=":wind_blowing_face:  Wind", value=f"`{winds}`", inline=True)
            metembed.add_field(name=":fog: Visibility", value=f"`{visibility}`", inline=True)
            metembed.add_field(name=":umbrella: Humidity", value=f"`{humidity}%`", inline=True)
            metembed.add_field(name=":cloud: Clouds", value=f"`{clouds}`", inline=True)
            metembed.add_field(name=":cloud_rain: Weather", value=f"`{condition}`", inline=True)
            metembed.add_field(name=":white_sun_small_cloud: Ceiling", value=f"`{ceiling}`", inline=True)
            metembed.add_field(name=":thermometer: Temperature", value=f"`{temp}°C/{temp_f}°F`", inline=True)
            metembed.add_field(name=":droplet: Dewpoint", value=f"`{dewpoint}°C/{dewpoint_f}°F`", inline=True)
            metembed.add_field(name=":chart_with_upwards_trend: Barometer", value=f"`{altimq}/{altima}`", inline=True)

            await interaction.followup.send(embed=metembed)


    @app_commands.command(
        name="taf",
        description="Fetch decoded TAF for airport!")
        
    async def taf(
        self,
        interaction: discord.Interaction,
        airport: str,
        private: bool = True
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=private)
        url = "https://api.checkwx.com/taf/"
        final_url = f"{url}{airport}{rule}"
        req = requests.get(final_url, headers=hdr).json()
        x = json.dumps(req)
        s = json.loads(x)
        for item in s['data']:
            station_id = item['station']['name']
            raw_taf = item['raw_text']
            taf = pytaf.TAF(raw_taf)
            decoder = pytaf.Decoder(taf)
            taf_embed = Embed(
                title=f"Decoded TAF for {item['icao']} aerodrome", 
                description=f"\nRAW TAF: `{item['raw_text']}`\n\n\n __Decoded TAF__\n\n**{decoder.decode_taf()}**\n\n", 
                colour=VATADR_BLUE
            )
            await interaction.followup.send(embed=taf_embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Metar(bot),
        guilds= [discord.Object(id=GUILD_ID)])
        
