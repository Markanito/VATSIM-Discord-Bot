import discord
import requests
import json
import utils.json_loader
import xml.etree.ElementTree as ET

from discord import Embed, Colour
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone, date, time
from helpers.config import GUILD_ID, VATADR_BLUE

callsign_prefix = utils.json_loader.read_json("callsign_prefix")
positions = ["GND","TWR","APP","CTR"]

class Controller():
    def __init__(self, callsign, booking_start, booking_end, booking_date):
        self.callsign = callsign
        self.booking_start = booking_start
        self.booking_end = booking_end
        self.booking_date = booking_date
    def get_callsign(self):
        return self.callsign
    def get_booking_start(self):
        return self.booking_start
    def get_booking_end(self):
        return self.booking_end
    def get_booking_date(self):
        return self.booking_date

class Bookings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="bookings",
        description="Display all future bookings"
    )
    async def bookings(
        self,
        interaction: discord.Interaction,
        private: bool = False
    ): 
        await interaction.response.defer(thinking=True, ephemeral=private)
        booked_2_obj = []
        booked_2_cs = []
        tree = ET.fromstring(requests.get('http://vatbook.euroutepro.com/xml2.php?fir=').text)
        bookings_exists = False
        for atcs in tree.find('atcs'):
            callsign = atcs.find('callsign').text
            time_start = atcs.find('time_start').text
            time_end = atcs.find('time_end').text
            booking_start = datetime.strptime(time_start, '%Y-%m-%d %H:%M:%S')
            booking_end = datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')

            #Time Builder, do not mess with the lines below
            booking_start_month = booking_start.month
            booking_start_day = booking_start.day
            booking_start_hour = booking_start.hour
            booking_start_minute = booking_start.minute
            booking_end_hour = booking_end.hour
            booking_end_minute = booking_end.minute

            if booking_start_month < 10:
                booking_start_month = f'0{booking_start_month}'
            if  booking_start_day < 10:
                booking_start_day = f'0{booking_start_day}'
            if booking_start_hour < 10:
                booking_start_hour = f'0{booking_start_hour}'
            if booking_start_minute < 10:
                booking_start_minute = f'0{booking_start_minute}'
            if booking_end_hour <10:
                booking_end_hour = f'0{booking_end_hour}'
            if booking_end_minute <10:
                booking_end_minute = f'0{booking_end_minute}'
            
            booking_start = f"{booking_start_hour}:{booking_start_minute}"
            booking_end = f"{booking_end_hour}:{booking_end_minute}"
            booking_date = f"{booking_start_day}.{booking_start_month}"

            embed = Embed(
                title=f"Bookings Table",
                color = VATADR_BLUE
            )
            for i in callsign_prefix:
                if i == callsign[:len(i)] and callsign[-3:] in positions:
                    controller_obj = Controller(callsign, booking_start, booking_end, booking_date)
                    booked_2_obj.append(controller_obj)
                    booked_2_cs.append(callsign)
                 
            for i in booked_2_obj:
                bookings_exists=True
                embed.add_field(
                    name=f":radio: {' '}C/S:{' '}`{i.get_callsign()}`{' '} |{' '}:date: Date: {' '}`{i.get_booking_date()}`{' '} | {' '} :timer: Start: `{i.get_booking_start()}z`{' '} | {' '}:timer:{' '}End: {' '}`{i.get_booking_end()}z`",
                    value=f"\uFEFF",
                    inline=False
                )

        if bookings_exists:
            await interaction.followup.send(embed=embed)
        else:
            embed.add_field(
                name=f":x: No bookings found.",
                value="\nFEFF",
                inline=False
            )
            await interaction.followup.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.\n-----")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Bookings(bot),
        guilds= [discord.Object(id=GUILD_ID)])
        
