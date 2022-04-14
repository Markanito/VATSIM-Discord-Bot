from re import M
import discord
import requests
import json
import utils.json_loader
import math

from datetime import datetime, date, time, timezone
from discord import Embed, Colour
from discord import app_commands
from discord.ext import commands
from helpers.config import GUILD_ID, VATADR_BLUE, VATADR_RED

airports = utils.json_loader.read_json("airports")

class Departures(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="departures",
        description="Get departers from desired airport"
    )
    async def departures(
        self,
        interaction: discord.Interaction,
        airport: str,
        private: bool = False
    ) -> None:
        await interaction.response.defer(thinking=True, ephemeral=private)
        if airport.upper() in airport:
            t = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
            xy = json.dumps(t)
            s = json.loads(xy)
            departures_exist = False
            embed = Embed(
                title=f"Departure Table for {airport.upper()}",
                color = VATADR_BLUE
            ) 
            for item in s['pilots']:
                if item['flight_plan'] != None:
                    if item['flight_plan']['departure'] == (airport.upper()):
                        if item['groundspeed'] < 30:
                            try:
                                departures_exist = True
                                callsign = item['callsign']
                                departure = item['flight_plan']['departure']
                                arrival = item['flight_plan']['arrival']
                                if item['flight_plan']['deptime'] == "0000":
                                    depa_time = f"Departure time unknown"
                                else:
                                    depa_time = item['flight_plan']['deptime']
                                    
                                embed.add_field(
                                    name=f":airplane: C/S:{' '} `{callsign}` {' '} | {' '}:airplane_departure: ADEP {' '}`{departure}`{' '} | {' '}:airplane_arriving: ADES: {' '}`{arrival}`{' '}| {' '} :clock1: ETD: {' '}`{depa_time}z`",
                                    value="\uFEFF",
                                    inline=False
                                )
                            except Exception as e:
                                embed.add_field(
                                    name=f"Failed to load arrivals",
                                    value=f"{e}",
                                    inline=False  
                                )
            if departures_exist:
                await interaction.followup.send(embed=embed)
            else:
                embed = Embed(
                title=f"Departure Table for {airport.upper()}",
                color = VATADR_RED
                )
                embed.add_field(
                    name=f":x: There is no departures at the moment :x:",
                    value="\uFEFF",
                    inline=False
                )

                await interaction.followup.send(embed=embed)

    @app_commands.command(
        name="alldepartures",
        description="Get all departures"
    )
    async def alldepartures(
        self,
        interaction = discord.Interaction,
        private: bool = False
    ):
        await interaction.response.defer(thinking=True, ephemeral=private)
        data = requests.get('https://data.vatsim.net/v3/vatsim-data.json').json()
        resp = json.dumps(data)
        s = json.loads(resp)    
        deparutres_exist = False
        embed = Embed(
            title="Departure Table",
            color = VATADR_BLUE,
        )
                    
        for item in s['pilots']:
            if item['flight_plan'] != None:
                if item['flight_plan']['departure'] in airports:
                    if item['groundspeed'] < 30:
                        try:
                            deparutres_exist=True
                            callsign = item['callsign']
                            departure = item['flight_plan']['departure']
                            arrival = item['flight_plan']['arrival']
                            if item['flight_plan']['deptime'] == "0000":
                                depa_time = f"Departure time unknown"
                            else:
                                depa_time = item['flight_plan']['deptime']
                                
                                
                            embed.add_field(
                                name=f":airplane: C/S:{' '} `{callsign}` {' '} | {' '}:airplane_departure: ADEP {' '}`{departure}`{' '} | {' '}:airplane_arriving: ADES: {' '}`{arrival}`{' '}| {' '} :clock1: ETD: {' '}`{depa_time}z`",
                                value="\uFEFF",
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                            name=f"Failed to load arrivals",
                                value=f"{e}",
                                inline=False
                            )
        if not deparutres_exist:
            embed = Embed(
                title=f"Departure Table",
                color = VATADR_RED
            )
            embed.add_field(
                name=f":x: There is no departures at the moment :x:",
                value="\uFEFF",
                inline=False
            )

            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Departures(bot),
        guilds= [discord.Object(id=GUILD_ID)])
        
